from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
import threading,subprocess,json,base64,io
import numpy as np
from PIL import Image,ImageDraw
from scipy.ndimage import label,find_objects
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1];before=b''
Path('/tmp/ze-motion-reference').mkdir(exist_ok=True)
reference=json.loads((root/'references'/'motion_observations_25fps.json').read_text())
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(root),**kw)
 def do_GET(self):
  if self.path=='/before.html':self.send_response(200);self.send_header('Content-Type','text/html');self.end_headers();self.wfile.write(before)
  else:super().do_GET()
server=ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
def measure(im):
 roi=im[60:495,500:935].astype(int);mask=(roi.max(2)-roi.min(2)<14)&(roi.min(2)>65);ids,count=label(mask);areas=np.bincount(ids.ravel());areas[0]=0
 if count and areas.max()>9:
  ys,xs=find_objects((ids==areas.argmax()).astype(np.uint8))[0];return xs.stop-xs.start
 return 0
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);page=browser.new_page(viewport={'width':1600,'height':1000});errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
  results={}
  for version in ['ZE_OS_Mouwajaha_V07.html']:
   page.goto(f'http://127.0.0.1:{server.server_port}/'+version);page.wait_for_function('assets.bg && assets.source && state.stvLoaded')
   page.locator('.control-panel').evaluate_all('(panels)=>panels.forEach(p=>p.open=true)')
   if version!='before.html':page.locator('#protectLowerThird').uncheck()
   page.locator('#modeReference').click()
   widths=[]
   for n in range(17,31):
    png=page.evaluate('(t)=>{setT(t);return cvs.toDataURL()}',n/25)
    im=np.array(Image.open(io.BytesIO(base64.b64decode(png.split(',')[1]))).convert('RGB').resize((960,540)))
    widths.append(measure(im))
   targets=[reference[n].get('outer',{}).get('w',0) for n in range(17,31)]
   mae=float(np.mean(np.abs(np.array(widths)-targets)));results[version]={'widths':widths,'target':targets,'mae':mae};print(version,'outer-width mean error',mae,flush=True)
  assert results['ZE_OS_Mouwajaha_V07.html']['mae']<1
  Path('/tmp/ze-motion-reference/validation.json').write_text(json.dumps(results,indent=2))
  # Validate protected group bounds through the entrance, resizing and manual offsets.
  page.locator('#protectLowerThird').check();page.locator('#safeAreas').check()
  for mode in ['normal','breaking']:
   page.locator('#lowerThirdMode').select_option(mode)
   for n in range(0,151):
    bounds=page.evaluate('(t)=>{setT(t);return {safe:zeBroadcastBounds(),boxes:[getBBox("identity"),getBBox("source"),getBBox("bullet")]}}',n/25)
    for box in bounds['boxes']:
     if box['w']:assert box['y']+box['h']<=bounds['safe']['bottom']+.01,(mode,n,box)
  page.evaluate("window.refBg=document.createElement('canvas');refBg.width=1920;refBg.height=1080;const bgc=refBg.getContext('2d',{alpha:false});setupCtx(bgc);cover(bgc,assets.bg,0,0,W,H)")
  def band_difference():
   return page.evaluate("(()=>{const y=Math.round(zeBroadcastBounds().bottom*2),height=1080-y,a=c.getImageData(0,y,1920,height).data,b=refBg.getContext('2d').getImageData(0,y,1920,height).data;let max=0;for(let i=0;i<a.length;i+=4){max=Math.max(max,Math.abs(a[i]-b[i]),Math.abs(a[i+1]-b[i+1]),Math.abs(a[i+2]-b[i+2]))}return max})()")
  page.locator('#protectLowerThird').uncheck();page.evaluate('setT(4)');assert band_difference()>0
  page.locator('#protectLowerThird').check()
  for n in range(151):
   page.evaluate('(t)=>setT(t)',n/25);assert band_difference()==0,n
  print('Painted pixels: lower-third band stays identical to background over 151 entrance frames',flush=True)
  page.evaluate('state.layers.source.y=150;state.layers.source.scale=1.8;setT(4)')
  bounds=page.evaluate('({safe:zeBroadcastBounds(),box:getBBox("source")})');assert bounds['box']['y']+bounds['box']['h']<=bounds['safe']['bottom']
  page.evaluate('state.layers.source.y=0;state.layers.source.scale=1;setT(1.44)');page.locator('#canvas').screenshot(path='/tmp/ze-motion-reference/new-1.44.png')
  page.evaluate('setT(4)');page.screenshot(path='/tmp/ze-motion-reference/new-safe-desktop.png')
  page.locator('#showBullets').uncheck();page.evaluate('setT(1.8)');page.locator('#canvas').screenshot(path='/tmp/ze-motion-reference/new-solo.png')
  assert not page.evaluate('state.renderError');assert not errors,errors;print('151 frames per safe preset, manual offsets/scales, solo layout, and JS errors: passed',flush=True);browser.close()
finally:server.shutdown();server.server_close()

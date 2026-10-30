"""Fixed V0.7 cadre across media shapes, Fill/Fit and independent post-text choices."""
from pathlib import Path
from http.server import ThreadingHTTPServer
import importlib.util, threading, json
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('helper',root/'ze_local_importer.py');helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
class Handler(helper.Handler):
 def do_GET(self):
  if self.path.startswith('/fixtures/'):return self._send_media(root/'tests/fixtures'/Path(self.path).name)
  super().do_GET()
server=ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);page=browser.new_page(viewport={'width':1920,'height':1080});errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
  page.goto(f'http://127.0.0.1:{server.server_port}/ZE_OS_Mouwajaha_V07.html');page.wait_for_function('state.stvLoaded && assets.source')
  assert page.locator('#portraitLayout').input_value()=='reference'
  baseline=page.evaluate("zeVisibleBounds('source',getBBox('source'))")
  print('Reference painted size:',baseline,flush=True)
  text='نص المنشور قابل للتحرير مع صورة أو فيديو https://t.co/example'
  for kind,src in [('video','/fixtures/portrait.mp4'),('video','/fixtures/landscape.mp4'),('image','/fixtures/photo.png'),('image',None)]:
   page.evaluate('''async(v)=>{let url=v.src;if(!url){const c=document.createElement('canvas');c.width=c.height=400;const x=c.getContext('2d');x.fillStyle='#168fb5';x.fillRect(0,0,400,400);url=c.toDataURL()}zeCommitPost(await zePreparePost({text:v.text,attachments:[{type:v.kind,url}]}));setT(5)}''',dict(kind=kind,src=src,text=text))
   if kind=='video':page.wait_for_function('zePost.items[0].el.readyState>=2 && !zePost.items[0].el.seeking')
   assert page.locator('#postMediaFit').input_value()=='fit' and page.locator('#postTextPlacement').input_value()=='roll'
   for flip in [False,True]:
    page.evaluate('(flip)=>setFlipped(flip)',flip)
    expected=page.evaluate('getBBox("source")')
    assert abs(expected['w']-baseline['w'])<.01 and abs(expected['h']-baseline['h'])<.01,(src,expected,baseline)
    for fitting in ['fill','fit']:
     page.locator('#postMediaFit').select_option(fitting)
     for placement in ['bullet','roll','hidden']:
      page.locator('#postTextPlacement').select_option(placement,force=True)
      boxes=page.evaluate('zeSafeLayout()');s,b,h=[boxes[key] for key in ['source','bullet','identity']];safe=page.evaluate('zeBroadcastBounds()')
      assert all(abs(s[k]-expected[k])<.01 for k in ['x','y','w','h']),(src,flip,fitting,placement,boxes)
      assert b['y']+b['h']<=safe['bottom']+.01 and h['y']+h['h']<=b['y']-11.99,boxes
      assert page.evaluate('Boolean(zePostRollText())')==(placement=='roll')
      dimensions=page.evaluate('''(()=>{const i=zePrimaryMedia(),p=zeProtectedPlacement({width:i.width,height:i.height},365,372,i);return {iw:i.width,ih:i.height,...p}})()''')
      if fitting=='fill':assert dimensions['w']>=365-.01 and dimensions['h']>=372-.01,dimensions
      else:assert dimensions['w']<=365+.01 and dimensions['h']<=372+.01 and abs(dimensions['scale']-dimensions['base'])<.00001,dimensions
    page.locator('#postTextPlacement').select_option('bullet',force=True);page.locator('#postMediaFit').select_option('fill')
   print(src or 'square generated photo','same frame, two flips, Fill/Fit and three text choices: passed',flush=True)
  # Painting rather than only dimensions: Fit retains both red/blue edges; Fill crops them.
  assert page.evaluate('''(()=>{const frame=document.createElement('canvas');frame.width=800;frame.height=200;const c=frame.getContext('2d');c.fillStyle='green';c.fillRect(0,0,800,200);c.fillStyle='red';c.fillRect(0,0,80,200);c.fillStyle='blue';c.fillRect(720,0,80,200);const out=document.createElement('canvas');out.width=out.height=400;const x=out.getContext('2d'),item={};let colors={};for(const mode of ['fill','fit']){document.getElementById('postMediaFit').value=mode;x.clearRect(0,0,400,400);zeDrawFramedMedia(x,frame,0,0,400,400,item);colors[mode]=[...x.getImageData(5,200,1,1).data,...x.getImageData(395,200,1,1).data]}document.getElementById('postMediaFit').value='fill';return colors.fill[1]===128&&colors.fill[5]===128&&colors.fit[0]===255&&colors.fit[6]===255})()''')
  assert page.evaluate('''(()=>{const p=zeProtectedPlacement({width:400,height:800},400,300,{framing:{zoom:100,protectFace:false,face:{x:0,y:70,w:25,h:30}}});return Math.abs(p.x-(400-p.w)/2)<.00001&&Math.abs(p.y-(300-p.h)/2)<.00001})()''')
  # Manual region remains available; it limits a crop only when enabled. Fit never crops.
  assert page.evaluate('''(()=>{const im={width:360,height:640},i={framing:{zoom:140,protectFace:true,face:{x:20,y:5,w:60,h:90}}};const fill=zeProtectedPlacement(im,400,300,i);document.getElementById('postMediaFit').value='fit';const fit=zeProtectedPlacement(im,400,300,i);document.getElementById('postMediaFit').value='fill';return fill.scale<=300/(.9*640)+.00001&&fit.scale===fit.base})()''')
  for enabled in [True,False]:
   page.evaluate('(v)=>{document.getElementById("protectLowerThird").checked=v;document.getElementById("allowMediaOverlap").checked=false;draw()}',enabled)
   page.locator('#showBullets').uncheck();assert page.evaluate('zeEmbeddedHeader()');s=page.evaluate('getBBox("source")');assert s['w']==baseline['w'] and s['h']<=baseline['h']+.01
   if enabled:assert page.evaluate('getBBox("source").y+getBBox("source").h<=zeBroadcastBounds().bottom+.01')
   page.locator('#showBullets').check()
  page.evaluate('document.getElementById("protectLowerThird").checked=false;setT(5)')
  for t in [0,.4,.8,1.2,1.6,2,2.5,3.5,49.96]:page.evaluate('(t)=>setT(t)',t);assert not page.evaluate('state.renderError')
  with page.expect_download() as output:page.locator('#saveJson').click()
  output.value.save_as('/tmp/ze-beta273.json');saved=json.loads(Path('/tmp/ze-beta273.json').read_text());assert saved['rollFrameSizing']=='reference' and saved['postMedia']['fit']=='fill'
  page.set_viewport_size({'width':780,'height':1000});assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  assert not errors,errors;browser.close();print('Painted crop/contain, manual face region, solo/header, strict safety, entrance frames and saved settings: passed',flush=True)
finally:server.shutdown();server.server_close()

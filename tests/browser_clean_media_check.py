"""Hidden post text centers protected media; structured layouts never add a blurred duplicate."""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
import threading
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1];server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(root)));threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);page=browser.new_page(viewport={'width':1920,'height':1080});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(f'http://127.0.0.1:{server.server_port}/ZE_OS_Mouwajaha_V07.html');page.wait_for_function('state.stvLoaded && assets.source')
  result=page.evaluate('''(()=>{const frame=document.createElement('canvas');frame.width=360;frame.height=640;const f=frame.getContext('2d');f.fillStyle='#0088ff';f.fillRect(0,0,360,640);f.fillStyle='#ff2200';f.fillRect(0,0,40,640);const item={type:'image',el:frame,width:360,height:640,framing:{zoom:140,protectFace:true,face:{x:40,y:20,w:60,h:40}}};const out=document.createElement('canvas');out.width=600;out.height=300;const ctx=out.getContext('2d'),measure=()=>{const a=ctx.getImageData(0,0,600,300).data;let l=600,r=0,t=300,b=0,nonwhite=0;for(let y=0;y<300;y++)for(let x=0;x<600;x++){const i=(y*600+x)*4;if(a[i]!==255||a[i+1]!==255||a[i+2]!==255){nonwhite++;l=Math.min(l,x);r=Math.max(r,x);t=Math.min(t,y);b=Math.max(b,y)}}return {l,r,t,b,nonwhite}};let answer={};for(const center of [true,false]){ctx.fillStyle='white';ctx.fillRect(0,0,600,300);zeDrawCleanMedia(ctx,frame,0,0,600,300,item,center);answer[center?'hidden':'withText']=measure()}return answer})()''')
  h=result['hidden'];assert abs((h['l']+h['r'])/2-299.5)<1 and abs((h['t']+h['b'])/2-149.5)<1 and h['r']-h['l']<171,result
  assert result['withText']['r']-result['withText']['l']<425 and result['withText']['nonwhite']<600*300,result
  text='نص المنشور يظل فوق منطقة الخبر العاجل، مع وسائط حادة دون خلفية مكررة ضبابية. '
  page.locator('#sourceFile').set_input_files(str(root/'tests/fixtures/portrait.png'));page.wait_for_function('zePost.active');page.locator('#postBody').fill(text*30)
  for whole in [False,True]:
   if whole:page.locator('#useWholePost').click()
   for placement in ['roll','hidden']:
    page.locator('#postTextPlacement').select_option(placement,force=True)
    report=page.evaluate('''(()=>{const old=zeDrawCleanMedia,calls=[];zeDrawCleanMedia=(ctx,im,x,y,w,h,item,center)=>{calls.push({x,y,w,h,center});old(ctx,im,x,y,w,h,item,center)};setT(5);zeDrawCleanMedia=old;return {calls,box:getBBox('source'),hidden:!zePostRollText()}})()''');assert report['calls'] and report['calls'][0]['center']==(placement=='hidden'),report
    if placement=='hidden':assert report['calls'][0]['w']>report['box']['w']*.85,report
   page.locator('#postTextPlacement').select_option('roll',force=True)
  assert not errors and not page.evaluate('state.renderError'),errors;browser.close();print('Protected media centers when text is hidden; no editor-generated blur with text; Main/Whole full-body centering and sharp media: passed',flush=True)
finally:server.shutdown();server.server_close()

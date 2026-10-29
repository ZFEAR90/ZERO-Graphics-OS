from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
import threading,json
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1];server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(root)));threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);page=browser.new_page(viewport={'width':1920,'height':1080});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(f'http://127.0.0.1:{server.server_port}/ZE_OS_Mouwajaha_V07.html');page.wait_for_function('assets.source && state.stvLoaded')
  page.locator('#postFiles').set_input_files([str(root/'tests/fixtures/portrait.mp4'),str(root/'tests/fixtures/photo.png')]);page.wait_for_function('zePost.items.length===2');page.locator('#postBody').fill('هذه مقالة طويلة تظل قابلة للتمرير بينما يبقى فيديو المتحدث مرئياً. '*20)
  pin=page.get_by_role('checkbox',name='Keep portrait.mp4 visible while post scrolls');assert pin.is_checked()
  assert page.evaluate('zePinnedVideos().length===1');assert page.evaluate('zePostDocument();zePost.blocks.every(block=>block.item.type!=="video")')
  targets=[]
  for time in [3,10,25,49]:
   targets.append(page.evaluate('''(t)=>{const canvas=document.createElement('canvas');canvas.width=960;canvas.height=540;const ctx=canvas.getContext('2d'),good=fit,video=zePost.items[0];let target=null;fit=(c,frame,x,y,w,h)=>{if(frame===video.el||frame===video.lastFrame)target={x,y,w,h};return good(c,frame,x,y,w,h)};zeDrawPost(ctx,100,100,500,300,t);fit=good;return target}''',time))
  assert all(target==targets[0] for target in targets) and targets[0]['h']>200,targets
  # Every video cell uses contain: the face cannot be cropped by source scrolling.
  page.locator('#postFiles').set_input_files(str(root/'tests/fixtures/landscape.mp4'));page.wait_for_function('zePost.items.length===3');assert page.evaluate('zePinnedVideos().length')==2
  regions=page.evaluate('zePinnedVideoRegions(zePinnedVideos(),100,100,500,300,true).cells.map(({x,y,w,h})=>({x,y,w,h}))');assert regions[0]['x']+regions[0]['w']<regions[1]['x'];assert all(r['y']>=192 and r['y']+r['h']<=400 for r in regions)
  pin.uncheck();assert page.evaluate('zePinnedVideos().length')==1;assert page.evaluate('zePostDocument();zePost.blocks.some(block=>block.item===zePost.items[0])')
  with page.expect_download() as scene:page.locator('#saveJson').click()
  scene.value.save_as('/tmp/ze-beta27-speaker.json');data=json.loads(Path('/tmp/ze-beta27-speaker.json').read_text());assert data['postMedia']['items'][0]['keepVisible'] is False and data['postMedia']['items'][2]['keepVisible'] is True
  page.locator('#postScreenshot').evaluate('(el)=>{el.disabled=false;el.checked=true}');assert page.evaluate('zePinnedVideos().length')==0
  assert not page.evaluate('state.renderError');assert not errors,errors;print('Speaker-safe video stays fixed while text/photos scroll; full-frame contain, multiple pinned videos, override and saved state: passed');browser.close()
finally:server.shutdown();server.server_close()

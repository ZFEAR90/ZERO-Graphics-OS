"""Flip preserves the close header/bullet gap, with corner safety and group movement."""
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
  def check():
   gaps=[]
   for protected in [False,True]:
    for flipped in [False,True]:
     for offset in [0,-10]:
      data=page.evaluate('''(v)=>{document.getElementById('protectLowerThird').checked=v.protected;document.getElementById('allowMediaOverlap').checked=true;state.screenOffsets.bullet={x:0,y:v.offset};setFlipped(v.flipped);setT(5);const head=getBBox('identity'),bullet=zeVisibleBounds('bullet',getBBox('bullet'));return {head,bullet,gap:bullet.y-head.y-head.h,area:zeBroadcastBounds()}}''',dict(protected=protected,flipped=flipped,offset=offset))
      assert abs(data['gap']-24)<.01,data
      if protected:assert data['head']['y']>=(34 if flipped else data['area']['y'])-.01,data
      gaps.append(data['gap'])
   assert max(gaps)-min(gaps)<.01
  check()
  page.locator('#sourceFile').set_input_files(str(root/'tests/fixtures/landscape.mp4'));page.wait_for_function('zePost.active');check()
  page.locator('#portraitLayout').select_option('focus',force=True);check()
  assert not errors and not page.evaluate('state.renderError'),errors;browser.close();print('Header stays 24 scene units above bulletin in both flips, reference/imported/adaptive, safety On/Off and group movement: passed',flush=True)
finally:server.shutdown();server.server_close()

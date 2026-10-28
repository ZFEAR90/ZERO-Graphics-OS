from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
import threading,json
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1];server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(root)));threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);page=browser.new_page(viewport={'width':1600,'height':1000});errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
  page.goto(f'http://127.0.0.1:{server.server_port}/ZE_OS_Mouwajaha_V07.html');page.wait_for_function('assets.source && state.stvLoaded');page.locator('.control-panel').evaluate_all('(els)=>els.forEach(el=>el.open=true)')
  page.locator('#postFiles').set_input_files(str(root/'tests/fixtures/portrait.mp4'));page.wait_for_function('zePost.active && zePost.items.length===1');page.evaluate('setT(4)');portrait=page.evaluate('getBBox("identity")');page.locator('#canvas').screenshot(path='/tmp/ze-motion-reference/fixed-portrait.png')
  page.locator('#sourceFile').set_input_files(str(root/'tests/fixtures/landscape.mp4'));page.wait_for_function('zePost.items[0].width===640');landscape=page.evaluate('getBBox("identity")')
  assert abs(portrait['w']-landscape['w'])<.01 and abs(portrait['h']-landscape['h'])<.01,(portrait,landscape)
  print('Header dimensions fixed across portrait/landscape:',portrait['w'],portrait['h'],flush=True)
  page.locator('#protectLowerThird').uncheck()
  def boxes():return page.evaluate('Object.fromEntries(["identity","source","bullet"].map(n=>[n,getBBox(n)]))')
  def drag(name,dx,dy):
   b=page.evaluate('(n)=>getBBox(n)',name);r=page.locator('#canvas').bounding_box();x=r['x']+(b['x']+b['w']/2)/960*r['width'];y=r['y']+(b['y']+b['h']/2)/540*r['height'];page.mouse.move(x,y);page.mouse.down();page.mouse.move(x+dx,y+dy,steps=8);page.mouse.up()
  page.locator('#selectBullet').click();before=boxes();drag('bullet',12,-8);after=boxes();assert before['source']==after['source'] and before['identity']==after['identity'];assert before['bullet']!=after['bullet']
  page.evaluate("selectLayer('identity');selectLayer('bullet',true)");before=boxes();drag('bullet',6,3);after=boxes();assert before['source']==after['source'];assert before['identity']!=after['identity'] and before['bullet']!=after['bullet']
  print('Selected subset moves only its chosen groups',flush=True)
  page.locator('#selectAll').click();before=boxes();drag('source',10,12);after=boxes();deltas=[(after[n]['x']-before[n]['x'],after[n]['y']-before[n]['y']) for n in before];assert all(abs(dx-deltas[0][0])<.01 and abs(dy-deltas[0][1])<.01 for dx,dy in deltas),deltas
  before=boxes();page.locator('#compositionUp').click();after=boxes();assert all(abs(after[n]['y']-before[n]['y']+10)<.01 for n in before)
  page.locator('#protectLowerThird').check();safe=page.evaluate('zeBroadcastBounds()');assert all(b['y']>=safe['y'] and b['y']+b['h']<=safe['bottom'] for b in boxes().values())
  print('Mouse bullet-only/all-group dragging, whole-composition Up, and safe constraints passed',flush=True)
  # Decoder starvation must reuse the previous loop frame, not paint a dark frame.
  page.evaluate('state.customBackground=assets.avatar;state.bgKind="image";draw()');before=page.evaluate('cvs.toDataURL()')
  page.evaluate('state.customBackground={tagName:"VIDEO",readyState:1,videoWidth:640,videoHeight:360};state.bgKind="video";draw()');assert before==page.evaluate('cvs.toDataURL()')
  page.evaluate('window.goodCompose=compose;compose=(ctx,t)=>{ctx.fillStyle="black";ctx.fillRect(0,0,W,H);throw new Error("test decoder delay")};draw()');assert before==page.evaluate('cvs.toDataURL()');assert page.locator('#renderStatus').is_visible()
  page.evaluate('compose=goodCompose;state.customBackground=null;state.bgKind="image";draw()');assert page.evaluate('!state.renderError')
  assert not errors,errors;print('Undecoded background and interrupted render both retain a complete preview frame; no JS errors',flush=True)
  browser.close()
finally:server.shutdown();server.server_close()

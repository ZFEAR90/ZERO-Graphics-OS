from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
import threading
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1];Path('/tmp/ze-motion-reference').mkdir(exist_ok=True);server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(root)));threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);page=browser.new_page(viewport={'width':1600,'height':1000});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(f'http://127.0.0.1:{server.server_port}/ZE_OS_Mouwajaha_V07.html');page.wait_for_function('assets.source && state.stvLoaded');page.locator('.control-panel').evaluate_all('(els)=>els.forEach(el=>el.open=true)')
  page.locator('.editor-tab-panel').evaluate_all('(els)=>els.forEach(el=>el.hidden=false)');page.locator('.element-overrides').evaluate_all('(els)=>els.forEach(el=>el.open=true)')
  page.evaluate('setT(1.44)');before=page.evaluate('cvs.toDataURL()')
  page.evaluate('zeSetPalette("#2555aa")');assert page.locator('#frameColor').input_value()!='#8f8f90';assert before!=page.evaluate('cvs.toDataURL()')
  page.locator('#canvas').screenshot(path='/tmp/ze-motion-reference/adaptive-gray.png')
  page.locator('#frameColor').evaluate('(el)=>{el.value="#c87722";el.dispatchEvent(new Event("input",{bubbles:true}))}')
  assert not page.locator('#adaptFrameColor').is_checked();page.evaluate('zeSetPalette("#22aa66")');assert page.locator('#frameColor').input_value()=='#c87722'
  page.locator('#restoreColors').click();assert page.locator('#frameColor').input_value()=='#8f8f90';assert page.locator('#adaptFrameColor').is_checked()
  page.locator('#safeAreas').check();show=page.evaluate('cvs.toDataURL()');page.locator('#safeAreas').uncheck();assert show==page.evaluate('cvs.toDataURL()')
  samples=page.evaluate('Array.from({length:101},(_,i)=>zeSampleTrack("gray",(26+12*i/100)/25))');assert samples[0]==0 and samples[-1]==1;assert all(b>=a for a,b in zip(samples,samples[1:]));assert max(b-a for a,b in zip(samples,samples[1:]))<.05
  page.locator('[data-panel="colors"] .element-overrides').evaluate('(el)=>el.open=true')
  assert page.locator('[data-panel="colors"] .colorgrid input[type="color"]').count()==3
  page.locator('#backgroundFile').set_input_files(str(root/'tests/fixtures/photo.png'))
  page.wait_for_function('zeSolo.palette!==null');accent1=page.locator('#accentColor').input_value()
  page.locator('#bulletPanelColor').evaluate('(el)=>{el.value="#774422";el.dispatchEvent(new Event("input",{bubbles:true}))}')
  assert page.locator('#bulletPanelOverride').is_checked()
  page.locator('#backgroundFile').set_input_files(str(root/'tests/fixtures/portrait.png'))
  page.wait_for_function('(previous)=>document.getElementById("accentColor").value!==previous',arg=accent1)
  assert page.evaluate('zeElementColor("bulletPanel")')=='#774422'
  page.locator('#accentColor').evaluate('(el)=>{el.value="#117755";el.dispatchEvent(new Event("input",{bubbles:true}))}')
  assert page.evaluate('zeElementColor("sourceAccent")')=='#117755'
  page.locator('#sourceAccentColor').evaluate('(el)=>{el.value="#8833aa";el.dispatchEvent(new Event("input",{bubbles:true}))}')
  page.locator('#accentColor').evaluate('(el)=>{el.value="#223399";el.dispatchEvent(new Event("input",{bubbles:true}))}')
  assert page.evaluate('zeElementColor("sourceAccent")')=='#8833aa'
  page.locator('#sourceAccentOverride').uncheck();assert page.evaluate('zeElementColor("sourceAccent")')=='#223399'
  page.screenshot(path='/tmp/ze-motion-reference/palette-controls.png')
  page.locator('#restoreColors').click();assert all(not page.locator('#'+key+'Override').is_checked() for key in page.evaluate('Object.keys(zeColorSpec)'))
  print('Actual loop changes auto-select three colors; master edits, persistent individual overrides, and reset passed')
  assert not page.evaluate('state.renderError');assert not errors,errors;print('Frame/mask adaptation, manual override, identity restore, preview-only safe guide, and continuous gray scale: passed')
  browser.close()
finally:server.shutdown();server.server_close()

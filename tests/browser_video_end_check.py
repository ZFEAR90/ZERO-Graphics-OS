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
  page.locator('#postFiles').set_input_files([str(root/'tests/fixtures/portrait.mp4'),str(root/'tests/fixtures/landscape.mp4')]);page.wait_for_function('zePost.items.length===2')
  first=page.get_by_role('combobox',name='After video ends for portrait.mp4');second=page.get_by_role('combobox',name='After video ends for landscape.mp4');assert first.input_value()=='hold' and second.input_value()=='hold'
  duration=page.evaluate('zePost.items[0].el.duration');page.evaluate('(t)=>setT(t)',1.88+duration*2+.5);page.wait_for_function('Math.abs(zePost.items[0].el.currentTime-zePost.items[0].el.duration+.02)<.01');assert page.evaluate('zePost.items[0].el.paused && !zePost.items[0].el.loop')
  first.select_option('loop');page.wait_for_function('Math.abs(zePost.items[0].el.currentTime-.5)<.02');assert page.evaluate('zePost.items[0].el.loop && !zePost.items[1].el.loop')
  page.locator('#play').click();page.wait_for_timeout(400);assert page.evaluate('!zePost.items[0].el.paused && zePost.items[1].el.paused');page.locator('#play').click()
  first.select_option('hold');page.wait_for_function('zePost.items[0].el.paused && !zePost.items[0].el.loop');page.wait_for_function('Math.abs(zePost.items[0].el.currentTime-zePost.items[0].el.duration+.02)<.01')
  second.select_option('loop');page.locator('#postAudio').check();page.wait_for_function('zePost.items[1].gain && zePost.items[1].el.loop');page.locator('#postVideos').uncheck();page.locator('#play').click();page.wait_for_timeout(250);assert page.evaluate('!zePost.items[1].el.paused && zePost.items[1].gain.gain.value===1');page.locator('#play').click()
  page.evaluate("const item=zePost.items[0];zePostFrame(item);window.heldFrame=item.lastFrame;Object.defineProperty(item.el,'readyState',{value:1,configurable:true})");assert page.evaluate('zePostFrame(zePost.items[0])===heldFrame');page.evaluate('delete zePost.items[0].el.readyState')
  with page.expect_download() as scene:page.locator('#saveJson').click()
  scene.value.save_as('/tmp/ze-beta27-video-end.json');data=json.loads(Path('/tmp/ze-beta27-video-end.json').read_text());assert [item['endBehavior'] for item in data['postMedia']['items']]==['hold','loop']
  assert not page.evaluate('state.renderError');assert not errors,errors;print('Independent hold/loop, seek past end, playback, hidden-video audio and saved settings: passed');browser.close()
finally:server.shutdown();server.server_close()

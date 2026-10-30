"""Compare portrait treatments, source-only overlap, flipping and uncropped media."""
from pathlib import Path
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from functools import partial
import threading, json
from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parents[1]
server = ThreadingHTTPServer(('127.0.0.1', 0), partial(SimpleHTTPRequestHandler, directory=str(root)))
threading.Thread(target=server.serve_forever, daemon=True).start()
try:
 with sync_playwright() as p:
  browser = p.chromium.launch(executable_path='/usr/bin/chromium', headless=True, args=['--no-sandbox'])
  page = browser.new_page(viewport={'width':1920, 'height':1080})
  errors = []; page.on('pageerror', lambda e: errors.append(str(e)))
  page.goto(f'http://127.0.0.1:{server.server_port}/ZE_OS_Mouwajaha_V07.html')
  page.wait_for_function('assets.source && state.stvLoaded');page.evaluate("document.querySelectorAll('.editor-tab-panel').forEach(e=>e.hidden=false);document.querySelectorAll('details').forEach(e=>e.open=true)")
  assert page.locator('#portraitLayout').input_value() == 'reference'
  page.locator('#portraitLayout').select_option('focus',force=True);page.locator('#postMediaFit').select_option('fit',force=True)
  assert not page.locator('#protectLowerThird').is_checked()
  page.locator('#respectSafeArea').click();assert page.locator('#protectLowerThird').is_checked() and not page.locator('#allowMediaOverlap').is_checked()
  page.locator('#allowMediaOverlap').check()
  page.locator('#postFiles').set_input_files(str(root/'tests/fixtures/portrait.png'))
  page.wait_for_function('zePost.active')
  page.locator('#postBody').fill('هذه فقرة توضيحية طويلة قابلة للتمرير وتبقى الصورة كاملة في كل وضع. '*30)
  page.evaluate('setT(5)')
  for mode in ['focus', 'portrait']:
   page.locator('#portraitLayout').select_option(mode,force=True)
   page.wait_for_timeout(80)
   for flip in [False, True]:
    page.evaluate('(v)=>setFlipped(v)', flip)
    data = page.evaluate('({boxes:zeSafeLayout(),area:zeBroadcastBounds(),centered:zeCenteredPortrait()})')
    s, h, b = (data['boxes'][n] for n in ['source', 'identity', 'bullet']); a = data['area']
    assert s['x'] >= a['x'] and s['x']+s['w'] <= a['x']+a['w']
    assert b['y']+b['h'] <= a['bottom']+.01 and h['y']+h['h'] <= a['bottom']+.01
    if mode in ['focus','portrait']:
     assert abs((min(b['x'],s['x'])+max(b['x']+b['w'],s['x']+s['w']))/2-480)<.01 and s['h']>=420
     assert a['top'] < s['y']+s['h'] <= 508 and b['w'] <= 280 and h['w'] < 310
     assert b['x'] > s['x']+s['w'] if flip else b['x']+b['w'] < s['x']
     assert 'overlap allowed' in page.locator('.broadcast-exclusion').first.inner_text()
    else:
     assert s['w'] >= 430 and abs(s['w']-b['w'])<40
     assert s['y']+s['h'] <= a['bottom']+.01
     assert 'overlap allowed' in page.locator('.broadcast-exclusion').first.inner_text()
    # A static picture stays fully visible at identical size while the text scrolls.
    targets = []
    for t in [5, 25, 49]:
     targets.append(page.evaluate('''(t)=>{const ctx=document.createElement('canvas').getContext('2d'),original=fit;let target=null;fit=(c,frame,x,y,w,h)=>{target={x,y,w,h};original(c,frame,x,y,w,h)};try{zeDrawPost(ctx,100,100,400,300,t)}finally{fit=original}return target}''', t))
    assert targets[0] and all(v==targets[0] for v in targets), (mode, targets)
    assert targets[0]['h']>230
    assert page.evaluate('zeSocialRegions(100,100,400,300).text.x+zeSocialRegions(100,100,400,300).text.w<zeSocialRegions(100,100,400,300).media.x')
   if mode=='beside':
    page.locator('#rollLanguage').select_option('ltr'); left=page.evaluate('zeRollDirection()'); assert left=='ltr'
    page.locator('#rollLanguage').select_option('rtl'); assert page.evaluate('zeRollDirection()')=='rtl'
   print(mode, 'portrait containment, safe areas and both flips: passed', flush=True)
  page.locator('#portraitLayout').select_option('focus',force=True)
  page.locator('#allowMediaOverlap').uncheck()
  assert page.evaluate('getBBox("source").y+getBBox("source").h<=zeBroadcastBounds().bottom')
  assert 'graphics excluded' in page.locator('.broadcast-exclusion').first.inner_text()
  page.locator('#allowMediaOverlap').check(); page.locator('#showBullets').uncheck()
  assert page.evaluate('getBBox("source").h>390 && getBBox("bullet").w===0')
  # Text-only now preserves the chosen media geometry; only its painted text is clamped.
  media_geometry=page.evaluate('getBBox("source")')
  page.locator('#postContentMode').select_option('text')
  assert page.evaluate('zeCenteredPortrait() && zeVisualItems().length===0 && zeLayoutMedia().length===1')
  assert page.evaluate('getBBox("source")')==media_geometry
  assert page.evaluate('zeSafeRollText()')
  page.locator('#postContentMode').select_option('all');assert page.evaluate('getBBox("source")')==media_geometry
  with page.expect_download() as output: page.locator('#saveJson').click()
  output.value.save_as('/tmp/ze-beta27-portrait.json')
  saved=json.loads(Path('/tmp/ze-beta27-portrait.json').read_text())
  assert saved['portraitLayout']=='focus' and saved['portraitLowerThirdOverlap'] is True
  # Ordinary landscape media keeps balanced widths; extra roll height is opt-out.
  page.locator('#sourceFile').set_input_files(str(root/'tests/fixtures/landscape.mp4'))
  page.wait_for_function('zePost.items.length===1 && zePost.items[0].label==="landscape.mp4"')
  page.locator('#postBody').fill('An editable caption remains separate from the complete landscape video. '*15)
  page.locator('#showBullets').check(); page.evaluate('setFlipped(false)')
  boxes=page.evaluate('zeSafeLayout()'); a=page.evaluate('zeBroadcastBounds()')
  assert boxes['source']['w']==460 and abs(boxes['source']['w']-boxes['bullet']['w'])<60
  assert boxes['source']['y']+boxes['source']['h']<=508
  page.evaluate('state.screenOffsets.source={x:0,y:100};draw()');assert page.evaluate('zeBroadcastBounds().top<getBBox("source").y+getBBox("source").h<=508')
  assert boxes['bullet']['y']+boxes['bullet']['h']<=a['bottom']+.01
  assert page.evaluate('zeHeaderPaintBounds(getBBox("identity")).y')>=76
  page.locator('#allowMediaOverlap').uncheck()
  assert page.evaluate('getBBox("source").y+getBBox("source").h<=zeBroadcastBounds().bottom')
  page.evaluate('setFlipped(true)'); assert page.evaluate('34<=zeHeaderPaintBounds(getBBox("identity")).y<76')
  print('Balanced landscape widths, shortened Live clearance, TV compensation and optional source-only overlap: passed',flush=True)
  # Main switch restores full-height bullets and unclips a full single photo.
  page.evaluate('state.screenOffsets.source={x:0,y:0}')
  page.locator('#respectSafeArea').click()
  assert not page.locator('#protectLowerThird').is_checked()
  page.locator('#sourceFile').set_input_files(str(root/'tests/fixtures/photo.png'))
  page.wait_for_function('zePost.items.length===1 && zePost.items[0].type==="image"')
  page.locator('#postBody').fill('A longer editable caption. '*20);page.locator('#postScrollMode').select_option('fixed')
  page.evaluate('setFlipped(false);setT(5)')
  assert page.evaluate('getBBox("bullet").h>180 && getBBox("bullet").y+getBBox("bullet").h<=zeBroadcastBounds().bottom+.01')
  assert page.evaluate('zePostDocument();zePost.blocks.length===0 && zeFixedPostMedia().includes(zePost.items[0])')
  photo=page.evaluate('''(()=>{const ctx=document.createElement('canvas').getContext('2d'),old=fit;let bounds=null;fit=(c,im,x,y,w,h)=>{bounds={w,h};old(c,im,x,y,w,h)};try{zeDrawPost(ctx,0,0,400,300,25)}finally{fit=old}return bounds})()''')
  region=page.evaluate('zeSocialRegions(0,0,400,300).media');assert photo['w']==region['w'] and photo['h']==region['h']
  page.locator('#respectSafeArea').click()
  assert page.evaluate('getBBox("bullet").y+getBBox("bullet").h<=zeBroadcastBounds().bottom')
  assert page.evaluate('getBBox("source").y+getBBox("source").h<=zeBroadcastBounds().bottom')
  assert page.locator('#respectSafeArea').get_attribute('aria-pressed')=='true'
  print('Safe bullet panel, full pinned photo, smaller header and strict/flexible Main switch: passed',flush=True)
  assert not page.evaluate('state.renderError') and not errors, errors
  browser.close()
finally:
 server.shutdown(); server.server_close()

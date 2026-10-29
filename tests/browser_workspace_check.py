"""Real UI checks for Main/Advanced, undo transactions and full-size safe placement."""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
import threading
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
server=ThreadingHTTPServer(('127.0.0.1',0),partial(SimpleHTTPRequestHandler,directory=str(root)))
threading.Thread(target=server.serve_forever,daemon=True).start()
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
  page=browser.new_page(viewport={'width':1920,'height':1080});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.goto(f'http://127.0.0.1:{server.server_port}/ZE_OS_Mouwajaha_V07.html');page.wait_for_function('assets.source && state.stvLoaded');page.evaluate('setT(6)');page.locator('#respectSafeArea').click()
  assert page.locator('#mainTab').get_attribute('aria-selected')=='true'
  assert page.locator('#bullets').is_visible() and page.locator('#displayname').is_visible()
  assert not page.locator('#advancedOptions').is_visible()
  page.locator('#bullets').fill('هذا نص عربي قابل للتحرير');page.locator('#advancedTab').click()
  assert page.locator('#advancedOptions').is_visible() and not page.locator('#mainOptions').is_visible()
  page.locator('[data-panel="colors"] summary').first.click();assert page.locator('#accentColor').is_visible()
  page.locator('#advancedTab').focus();page.keyboard.press('ArrowLeft');assert page.locator('#bullets').input_value()=='هذا نص عربي قابل للتحرير'
  def boxes():return page.evaluate('Object.fromEntries(["identity","source","bullet"].map(n=>[n,getBBox(n)]))')
  def drag(name,dx,dy):
   page.locator('#canvas').scroll_into_view_if_needed();b=page.evaluate('(n)=>getBBox(n)',name);r=page.locator('#canvas').bounding_box();x=r['x']+(b['x']+b['w']/2)/960*r['width'];y=r['y']+(b['y']+b['h']/2)/540*r['height'];page.mouse.move(x,y);page.mouse.down();page.mouse.move(x+dx,y+dy,steps=12);page.mouse.up()
  # Requested widths/scales survive protection; only the tall viewing window changes.
  for flipped in [False,True]:
   page.locator('#flip').set_checked(flipped);raw=page.evaluate('Object.fromEntries(["source","bullet","identity"].map(n=>[n,zeBeforeSafeBBox(n)]))');actual=boxes()
   assert all(abs(raw[n]['w']-actual[n]['w'])<.01 for n in ['source','bullet'])
   factor=.85*(1 if flipped else .95);assert abs(raw['identity']['w']*factor-actual['identity']['w'])<.01 and abs(raw['identity']['h']*factor-actual['identity']['h'])<.01
   safe=page.evaluate('zeBroadcastBounds()');paint=page.evaluate('Object.fromEntries(["source","bullet","identity"].map(n=>[n,zeVisibleBounds(n,getBBox(n))]))')
   assert all(b['x']>=safe['x']-.01 and b['x']+b['w']<=safe['x']+safe['w']+.01 for b in paint.values()),paint
   assert all(b['y']>=(34 if b['x']>=safe['x']+114 else safe['y'])-.01 and b['y']+b['h']<=safe['bottom']+.01 for b in paint.values()),paint
   assert paint['identity']['y']>=(34 if flipped else safe['y']) # The shorter Live reservation ends at the title-safe top.
  page.locator('#advancedTab').click();page.locator('[data-panel="layout"] summary').click();before=boxes();page.locator('#headerGroupScale').fill('80');page.locator('#headerGroupScale').press('Tab');assert abs(boxes()['identity']['w']/before['identity']['w']-80/85)<.001;page.locator('#undoEdit').click();assert boxes()==before;page.locator('#mainTab').click()
  page.locator('#flip').uncheck();page.locator('[data-panel="placement"] summary').click();before=boxes();page.locator('#compositionUp').click();after=boxes();assert all(abs(after[n]['y']-before[n]['y']+10)<.01 for n in before);page.locator('#undoEdit').click();assert boxes()==before;page.locator('[data-panel="placement"] summary').click();page.locator('#advancedTab').click();page.locator('[data-panel="guides"] summary').click();page.locator('#protectLowerThird').uncheck();page.locator('#mainTab').click()
  page.evaluate("selectLayer('bullet')");before=boxes();depth=page.evaluate('zeUndoStack.length');drag('bullet',-15,-12);after=boxes()
  assert before['source']==after['source'] and before['identity']!=after['identity'] and before['bullet']!=after['bullet']
  assert page.evaluate('zeUndoStack.length')==depth+1
  page.keyboard.press('Control+z');assert boxes()==before
  page.locator('#redoEdit').click();assert boxes()==after
  page.locator('#undoEdit').click();assert boxes()==before
  # A new branch of edits clears redo; a group move restores in one undo.
  page.evaluate("document.getElementById('selectAll').click()");before=boxes();drag('source',-8,-6);after=boxes();assert page.locator('#redoEdit').is_disabled()
  deltas=[(after[n]['x']-before[n]['x'],after[n]['y']-before[n]['y']) for n in before]
  assert all(abs(dx-deltas[0][0])<.01 and abs(dy-deltas[0][1])<.01 for dx,dy in deltas)
  page.keyboard.press('Control+z');assert boxes()==before
  page.keyboard.press('Control+Shift+z');assert boxes()==after
  # Up/Down and numeric movement are undoable too.
  page.locator('[data-panel="placement"] summary').click();before=boxes();page.locator('#compositionUp').click();assert boxes()!=before;page.locator('#undoEdit').click();assert boxes()==before
  before=boxes();page.locator('#compositionY').fill('-40');page.locator('#compositionY').press('Tab');assert boxes()!=before;page.locator('#undoEdit').click();assert boxes()==before
  # Ctrl+Z in a text editor remains the browser's text undo and does not undo movement.
  before=boxes();depth=page.evaluate('zeUndoStack.length');page.locator('#bullets').focus();page.keyboard.press('End');page.keyboard.type(' EXTRA');page.keyboard.press('Control+z');assert boxes()==before and page.evaluate('zeUndoStack.length')==depth
  page.locator('#advancedTab').click();page.locator('#protectLowerThird').check();page.locator('#mainTab').click();page.locator('#canvas').scroll_into_view_if_needed();page.screenshot(path='/tmp/ze-beta25-workspace.png')
  assert page.locator('#singleRebuild .broadcast-exclusion').is_visible()
  assert page.locator('#singleRebuild .broadcast-outline').is_visible()
  assert page.locator('#singleRebuild .broadcast-corner').count()==2
  assert page.locator('#singleRebuild .broadcast-corner').last.evaluate('(el)=>parseFloat(el.style.top)+parseFloat(el.style.height)')<=34/540*100+.01
  pixels=page.evaluate('cvs.toDataURL()');page.evaluate("document.getElementById('safeAreas').checked=false;zeUpdateSafePreview();draw()");assert pixels==page.evaluate('cvs.toDataURL()')
  page.set_viewport_size({'width':780,'height':1000});page.locator('#mainTab').click();assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  assert not page.evaluate('state.renderError');assert not errors,errors
  print('Main/Advanced, full-width safe flip, corner/side/lower-third guides, per-drag and multi-group undo/redo, numeric edits, native text undo, mobile width: passed')
  browser.close()
finally:server.shutdown();server.server_close()

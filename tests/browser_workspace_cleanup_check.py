"""Focused Beta 2.7.8 owner regression."""
from browser_support import scene
with scene('workspace') as s:
 p=s.page;s.post();
 for id in ['postUrl','postFiles','showBullets','postTextPlacement','postMediaFit','mainDuration','accentColor','saveJson','loadJson']:
  assert p.locator('#'+id).evaluate("e=>e.closest('.editor-tab-panel').id")=='mainOptions',id
 for id in ['compositionX','fontSize','postJustifyMode','mediaPresentation','frameColor','advancedPostMediaList','safeAreas']:
  assert p.locator('#'+id).evaluate("e=>e.closest('.editor-tab-panel').id")=='advancedOptions',id
 assert p.locator('.sidebar.right').count()==0 and p.locator('#renderVideo').is_visible()
 assert p.locator('[data-panel=aep]').evaluate('e=>!e.open') and p.locator('[data-panel=timing]').evaluate('e=>!e.open')
 p.locator('#openMediaDetails').click();assert p.locator('#advancedMediaPanel').evaluate('e=>e.open');assert p.locator('#advancedTab').get_attribute('aria-selected')=='true'
 p.locator('#mainTab').click();p.set_viewport_size({'width':780,'height':1000});assert p.evaluate('document.documentElement.scrollWidth<=innerWidth');assert p.locator('#canvas').bounding_box()['y']<p.locator('.sidebar').bounding_box()['y']
 print('Main essentials, Advanced details, live control listeners, collapsed references, render/export and narrow layout: passed')

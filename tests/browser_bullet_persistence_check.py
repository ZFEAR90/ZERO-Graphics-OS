"""Focused Beta 2.7.8 owner regression."""
from browser_support import scene
with scene('bullet-persistence') as s:
 p=s.page;s.post('Post body');s.value('bullets','Independent editorial text')
 for flip in [False,True]:
  p.evaluate('(v)=>setFlipped(v)',flip)
  for choice in ['roll','hidden','bullet','roll']:
   s.value('postTextPlacement',choice)
   if choice=='bullet':assert p.locator('#bullets').input_value()=='Post body'
   assert p.locator('#showBullets').is_checked() and p.evaluate("getBBox('bullet').w>0")
  assert p.locator('#bullets').input_value()=='Post body'
  s.value('showBullets',False);assert p.evaluate("getBBox('bullet').w===0");s.value('showBullets',True)
  original=p.locator('#bullets').input_value();p.locator('#useWholePost').click();assert not p.locator('#showBullets').is_checked() and p.locator('#bullets').input_value()==original
  assert p.evaluate("getBBox('source').w>600&&getBBox('bullet').w===0")
  p.locator('#useMainRoll').click();assert p.locator('#showBullets').is_checked() and p.locator('#bullets').input_value()==original
 s.value('bulletSplitMode','blank');s.value('bullets','First paragraph\n\nSecond paragraph');p.evaluate('zeParagraphModel.items[1].manual=6;zeParagraphModel.cache=null');holds=p.evaluate('zeParagraphSchedule().rows.map(r=>({text:r.text,manual:r.manual}))')
 p.locator('#useWholePost').click();assert p.evaluate('zeParagraphSchedule().rows.map(r=>({text:r.text,manual:r.manual}))')==holds
 p.locator('#useMainRoll').click();assert p.evaluate('zeParagraphSchedule().rows.map(r=>({text:r.text,manual:r.manual}))')==holds
 print('Placement preserves bullets; explicit hide works; Whole auto-hides without deleting text; Main restores visibility: passed')

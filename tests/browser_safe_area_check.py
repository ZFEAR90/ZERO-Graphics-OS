"""Focused Beta 2.7.8 owner regression."""
from browser_support import scene
with scene('safe-area') as s:
 p=s.page;s.post('Safe post text. '*100);s.value('bullets','نص آمن في لوحة الأخبار. '*100)
 for flip in [False,True]:
  p.evaluate('(v)=>setFlipped(v)',flip)
  for safe in [False,True]:
   s.value('protectLowerThird',safe);s.value('allowMediaOverlap',not safe)
   assert p.evaluate('zeBulletTextBox().y+zeBulletTextBox().h<=zeTextSafeBottom()+.01')
   if safe:assert p.evaluate('getBBox("source").y+getBBox("source").h<=zeBroadcastBounds().bottom+.01')
   else:assert p.evaluate('getBBox("source").y+getBBox("source").h>zeBroadcastBounds().top')
 p.locator('#useWholePost').click()
 for enabled in [False,True]:
  s.value('protectLowerThird',enabled);s.value('allowMediaOverlap',False);p.evaluate('state.screenOffsets.source.y=0;draw()');before=s.boxes()['source'];p.evaluate('state.screenOffsets.source.y=-20;draw()');assert s.boxes()['source']['y']<before['y']
 print('Mandatory bullet/text boundary, strict/flexible roll geometry, both flips and upward centered-roll movement: passed')

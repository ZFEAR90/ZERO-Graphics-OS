"""Focused Beta 2.7.8 owner regression."""
from browser_support import scene
with scene('text-only') as s:
 p=s.page
 for layout in ['reference','social']:
  s.value('portraitLayout',layout);s.post('Safe text inside the roll. '*70)
  for flip in [False,True]:
   p.evaluate('(v)=>setFlipped(v)',flip)
   for bullets in [False,True]:
    s.value('showBullets',bullets);before=s.boxes();s.value('postContentMode','text');assert s.boxes()==before
    assert p.evaluate('zePost.layoutMedia.length===1')
    s.value('postContentMode','all');assert s.boxes()==before
    if not bullets:assert abs(before['source']['x']+before['source']['w']/2-480)<12
 print('Text only has no upward jump, retained media geometry and centered solo composition in both flips: passed')

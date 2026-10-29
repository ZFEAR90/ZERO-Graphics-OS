"""Focused Beta 2.7.8 owner regression."""
from browser_support import scene
with scene('drag-undo') as s:
 p=s.page;s.post();s.value('protectLowerThird',False);p.evaluate("document.getElementById('compositionY').value=-60;setT(5)")
 for name in ['source','bullet','identity','all']:
  if name=='all':p.evaluate("document.getElementById('selectAll').click()")
  else:p.evaluate('(n)=>selectLayer(n)',name)
  before=s.boxes();s.drag('source' if name=='all' else name);after=s.boxes();assert before!=after,name
  if name=='source':assert before['bullet']==after['bullet'] and before['identity']==after['identity']
  if name=='bullet':assert before['source']==after['source'] and before['identity']!=after['identity']
  if name=='identity':assert before['source']==after['source'] and before['bullet']==after['bullet']
  p.keyboard.press('Control+z');assert s.boxes()==before,name
  p.keyboard.press('Control+Shift+z');assert s.boxes()==after,name
  p.locator('#undoEdit').click();assert s.boxes()==before
  p.locator('#redoEdit').click();assert s.boxes()==after
  p.locator('#undoEdit').click()
 p.locator('#useWholePost').click()
 for bullets in [False,True]:
  s.value('showBullets',bullets);p.evaluate("selectLayer('source');setT(5)");before=s.boxes();s.drag('source');after=s.boxes();assert before['source']!=after['source'] and before['identity']!=after['identity'];assert before['bullet']==after['bullet'];assert abs(after['identity']['x']-before['identity']['x']-(after['source']['x']-before['source']['x']))<.01
  p.keyboard.press('Control+z');assert s.boxes()==before
 print('Roll/bullet/header/all actual drags; exact keyboard and button Undo/Redo; logical groups: passed')

"""Temporary real pointer resizing: reflow, per-axis frame sizes, safe limits, undo and JSON."""
from browser_support import scene
with scene('mouse-resize') as s:
 p=s.page;s.post('نص طويل يتحرك مع الصورة ويحافظ على المعنى. '*40,('portrait.png',));s.all_controls()
 def resize(name,axis,dx,dy):
  p.evaluate('(name)=>{selectLayer(name);setT(5)}',name)
  handle=p.locator(f'.mouse-resize-handle[data-group="{name}"][data-axis="{axis}"]');handle.wait_for(state='visible');handle.scroll_into_view_if_needed();r=handle.bounding_box();p.mouse.move(r['x']+r['width']/2,r['y']+r['height']/2);p.mouse.down();p.mouse.move(r['x']+r['width']/2+dx,r['y']+r['height']/2+dy,steps=8);p.mouse.up()
 for flip in [False,True]:
  s.value('flip',flip)
  before=s.boxes()['source'];resize('source','e',-50,0);after=s.boxes()['source'];assert after['w']<before['w']-20,(before,after)
  assert abs(after['h']-before['h'])<1
  assert p.evaluate("zeSocialRegions(0,0,300,300).text!==null&&document.getElementById('postMediaFit').value==='fit'")
  p.locator('#undoEdit').click();assert abs(s.boxes()['source']['w']-before['w'])<1
  p.locator('#redoEdit').click();assert abs(s.boxes()['source']['w']-after['w'])<1
  p.locator('#resetMouseSizes').click()
  before=s.boxes()['bullet'];resize('bullet','se',-35,-25);after=s.boxes()['bullet'];assert after['w']<before['w']-15 and after['h']<before['h']-10,(before,after)
  assert p.evaluate('zeBulletTextBox().y+zeBulletTextBox().h<=zeTextSafeBottom()&&zeParagraphSchedule().rows.length>1')
  assert p.evaluate("(()=>{const b=getBBox('bullet'),h=zeHeaderPaintBounds(getBBox('identity'));return h.w<=b.w+.01&&h.y+h.h<=b.y-11.99})()")
  saved=p.evaluate('zeProjectData()');p.locator('#resetMouseSizes').click();p.evaluate('async data=>zeApplyProject(data)',saved);assert abs(s.boxes()['bullet']['w']-after['w'])<1
  p.locator('#resetMouseSizes').click()
 p.locator('#useWholePost').click();before=p.evaluate('zeSocialTextDocument(240).lines.length');resize('source','se',-80,-30)
 assert p.evaluate("state.layers.source.size.w>0&&!zeScrollTogether()")
 assert p.evaluate('zeSocialTextDocument(240).lines.length')!=before
 assert p.evaluate("(()=>{const s=getBBox('source'),h=getBBox('identity'),k=h.w/R.identity.w,l=zeNativePostLayout(c);return [l.avatar,l.name,l.handle].every(b=>{const x=h.x+(b.x-R.identity.x)*k,y=h.y+(b.y-R.identity.y)*k;return x>=s.x&&x+b.w*k<=s.x+s.w&&y>=s.y&&y+b.h*k<=s.y+s.h})})()")
 s.value('mouseResize',False);p.wait_for_function("!document.querySelector('.mouse-resize-handle')")
 print('Real pointer width/height resizing, normal/flip, text reflow, native header containment, safe capacity, Undo/Redo/reset and JSON round-trip: passed')

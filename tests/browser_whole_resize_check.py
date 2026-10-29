"""Focused Beta 2.7.8 owner regression."""
from browser_support import scene
with scene('whole-resize') as s:
 p=s.page;s.post('Long post text that reflows within the resized Whole roll frame. '*150);p.locator('#useWholePost').click();assert not p.locator('#showBullets').is_checked()
 for flip in [False,True]:
  p.evaluate('(v)=>setFlipped(v)',flip);widths=[]
  for scale in [.65,1,1.15]:
   result=p.evaluate("""v=>{state.layers.source.scale=v;setT(5);const b=getBBox('source'),w=b.w*365/402,h=b.h*372/398,regions=zeSocialRegions(0,zeSocialBand(),w,h-zeSocialBand()),doc=zeSocialTextDocument(regions.text.w);return {frame:b.w,doc:doc.width,text:regions.text.w,lines:doc.lines.length,media:regions.media}}""",scale)
   assert abs(result['doc']-result['text'])<=1;assert result['media']['x']+result['media']['w']<=result['frame'];widths.append(result)
  assert widths[0]['frame']<widths[1]['frame']<widths[2]['frame'] and widths[0]['lines']>widths[2]['lines']
  old=p.evaluate('zeSocialTextDocument(300).canvas.toDataURL()');p.evaluate('setT(25)');assert p.locator('#postScrollMode').input_value()=='together' and old==p.evaluate('zeSocialTextDocument(300).canvas.toDataURL()')
 print('Whole auto-hides bullet, resizes frame, rewraps long content responsively and rolls source text without rewriting it in both flips: passed')

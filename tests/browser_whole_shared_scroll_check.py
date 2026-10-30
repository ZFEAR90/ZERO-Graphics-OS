"""Focused Beta 2.7.8 owner regression."""
from browser_support import scene
with scene('whole-scroll') as s:
 p=s.page;s.post('Long post content scrolls as one masked roll. '*100,('landscape.mp4',));p.locator('#useWholePost').click();assert p.locator('#postScrollMode').input_value()=='together'
 for flip in [False,True]:
  p.evaluate('(v)=>setFlipped(v)',flip)
  for layout in ['right','below']:
   s.value('wholeFrameArrangement',layout)
   seen=p.evaluate("""()=>{const a=zeDrawSocialText,b=zeDrawPostMediaRegion,seen=[];zeDrawSocialText=(c,r)=>seen.push({kind:'text',y:r.y});zeDrawPostMediaRegion=(c,r)=>seen.push({kind:'media',y:r.y});for(const t of [5,20,49.96])zeDrawSocialPost(c,100,100,600,300,t);zeDrawSocialText=a;zeDrawPostMediaRegion=b;return seen}""")
   if layout=='below':assert seen[2]['y']<seen[0]['y'] and abs((seen[2]['y']-seen[0]['y'])-(seen[3]['y']-seen[1]['y']))<.01
   else:assert seen[3]['y']==seen[1]['y']
 s.value('wholeFrameArrangement','right');s.all_controls();pin=p.get_by_role('checkbox',name='Keep landscape.mp4 visible while post scrolls');assert pin.is_checked() and pin.is_disabled()
 coords=p.evaluate("""()=>{const old=zeDrawPostMediaRegion,a=[];zeDrawPostMediaRegion=(c,b)=>a.push(b.y);for(const t of [5,30])zeDrawSocialPost(c,0,100,600,300,t);zeDrawPostMediaRegion=old;return a}""");assert coords[0]==coords[1]
 s.value('wholeFrameArrangement','below');assert p.evaluate('zeScrollTogether()');assert not pin.is_checked() and pin.is_disabled()
 print('Whole right media fixed; below text/media share travel with constant spacing; arrangement controls the speaker policy: passed')

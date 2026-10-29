"""Focused Beta 2.7.8 owner regression."""
from browser_support import scene
with scene('whole-scroll') as s:
 p=s.page;s.post('Long post content scrolls as one masked roll. '*100,('landscape.mp4',));p.locator('#useWholePost').click();assert p.locator('#postScrollMode').input_value()=='together'
 for flip in [False,True]:
  p.evaluate('(v)=>setFlipped(v)',flip)
  for layout in ['right','below']:
   s.value('wholeFrameArrangement',layout)
   seen=p.evaluate("""()=>{const a=zeDrawSocialText,b=zeDrawPostMediaRegion,seen=[];zeDrawSocialText=(c,r)=>seen.push({kind:'text',y:r.y});zeDrawPostMediaRegion=(c,r)=>seen.push({kind:'media',y:r.y});for(const t of [5,20,49.96])zeDrawSocialPost(c,100,100,600,300,t);zeDrawSocialText=a;zeDrawPostMediaRegion=b;return seen}""")
   assert seen[2]['y']<seen[0]['y'] and abs((seen[2]['y']-seen[0]['y'])-(seen[3]['y']-seen[1]['y']))<.01
 s.value('wholeFrameArrangement','right');s.all_controls();p.get_by_role('checkbox',name='Keep landscape.mp4 visible while post scrolls').check();assert p.locator('#postScrollMode').input_value()=='fixed'
 coords=p.evaluate("""()=>{const old=zeDrawPostMediaRegion,a=[];zeDrawPostMediaRegion=(c,b)=>a.push(b.y);for(const t of [5,30])zeDrawSocialPost(c,0,100,600,300,t);zeDrawPostMediaRegion=old;return a}""");assert coords[0]==coords[1]
 p.get_by_role('checkbox',name='Keep landscape.mp4 visible while post scrolls').uncheck();assert p.locator('#postScrollMode').input_value()=='together'
 print('Whole right/below content rolls together with constant spacing; speaker-safe media pins and unpins: passed')

"""Focused Beta 2.7.8 owner regression."""
from browser_support import scene
with scene('media-only') as s:
 p=s.page
 for file in ['portrait.png','photo.png',None]:
  if file:s.post('Text https://t.co/hidden', (file,))
  else:p.evaluate("async()=>{const image=document.createElement('canvas');image.width=image.height=400;image.getContext('2d').fillRect(0,0,400,400);zeCommitPost(await zePreparePost({text:'Square post https://t.co/hidden',attachments:[{type:'image',data_url:image.toDataURL()}]}))}")
  assert 'https' not in p.evaluate('zePostRollText()')
  before=s.boxes()['source']
  for flip in [False,True]:
   p.evaluate('(v)=>setFlipped(v)',flip);s.value('postTextPlacement','hidden');assert p.evaluate('zePostRollText()')=='';assert s.boxes()['source']['w']==before['w'] and s.boxes()['source']['h']==before['h']
   for mode in ['fill','fit']:
    s.value('postMediaFit',mode)
    data=p.evaluate("(()=>{const i=zeVisualItems()[0],p=zeProtectedPlacement(i.el,365,372,i);return {w:p.w,h:p.h}})()")
    if mode=='fill':assert data['w']>=365-.01 and data['h']>=372-.01
    else:assert data['w']<=365+.01 and data['h']<=372+.01
   assert p.evaluate("(()=>{const i=zeVisualItems()[0],a=document.createElement('canvas');a.width=600;a.height=300;const ctx=a.getContext('2d');let blurred=false;const f=Object.getOwnPropertyDescriptor(CanvasRenderingContext2D.prototype,'filter');Object.defineProperty(ctx,'filter',{get(){return f.get.call(ctx)},set(v){blurred ||= v.includes('blur');f.set.call(ctx,v)}});zeDrawPostMediaRegion(ctx,{x:0,y:0,w:600,h:300},5,[i],true);return !blurred})()")
 print('Portrait/wide fixed frames, centered hidden text, Fill/Fit coverage, cleaned links and no generated blur: passed')

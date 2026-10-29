"""Focused Beta 2.7.8 owner regression."""
from browser_support import scene
with scene('media-sequence') as s:
 p=s.page
 result=p.evaluate("""()=>{const make=(color,marker)=>{const el=document.createElement('canvas');el.width=el.height=100;const x=el.getContext('2d');x.fillStyle=color;x.fillRect(0,0,100,100);x.fillStyle=marker;x.fillRect(5,20,15,60);return {el,type:'image',width:100,height:100,label:color}},items=[make('red','lime'),make('blue','yellow')],out=document.createElement('canvas');out.width=out.height=100;const x=out.getContext('2d'),slot=(timeline(DURATION)-val('sourceTiming')-1.88)/2,rows=[];for(const flip of [false,true]){setFlipped(flip);for(const time of [slot-.01,slot+.4,slot+.81,100]){x.clearRect(0,0,100,100);zeDrawPostMediaRegion(x,{x:0,y:0,w:100,h:100},time+1.88,items);const a=x.getImageData(3,3,94,94).data;rows.push({flip,time,opaque:Array.from(a).filter((_,i)=>i%4===3).every(v=>v===255),left:[...x.getImageData(10,50,1,1).data],right:[...x.getImageData(90,50,1,1).data]})}}document.getElementById('mediaPresentation').value='grid';const grid=zeMediaSequence(5,items).layers.length;return {rows,grid}}""")
 rows=result['rows'];assert all(r['opaque'] for r in rows)
 assert rows[0]['left'][:3]==[0,255,0] and rows[0]['right'][:3]==[255,0,0]
 assert rows[1]['left'][:3]==[255,255,0] and rows[1]['right'][:3]==[255,0,0]
 assert rows[5]['left'][:3]==[0,255,0] and rows[5]['right'][:3]==[0,0,255]
 for i in [2,3,6,7]:assert rows[i]['left'][:3]==[255,255,0] and rows[i]['right'][:3]==[0,0,255]
 assert result['grid']==2
 print('Before/during/after opaque masks, asymmetric unmirrored markers, reversed flip wipe, final hold and explicit grid: passed')

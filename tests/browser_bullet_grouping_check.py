"""Focused Beta 2.7.8 owner regression."""
from browser_support import scene
with scene('bullet-grouping') as s:
 p=s.page;s.post();s.value('bullets','فقرة قصيرة\n\nفقرة ثانية');assert p.evaluate('zeParagraphSchedule().rows.length')==1
 s.value('bulletSplitMode','blank');assert p.evaluate('zeParagraphSchedule().rows.length')==2
 p.evaluate('zeParagraphModel.items[1].manual=6;zeParagraphModel.cache=null');s.value('bullets','تم تعديل الأولى\n\nفقرة ثانية');assert p.evaluate('zeParagraphSchedule().rows[1].manual')==6
 s.value('bulletSplitMode','auto');s.value('bullets','هذا نص طويل لقياس السعة الحقيقية وحماية منطقة الأخبار. '*100)
 assert p.evaluate('zeParagraphSchedule().rows.length')>2
 assert p.evaluate('zeParagraphSchedule().rows.every(r=>r.lineCount<=Math.floor((zeBulletTextBox().h-zeBulletTextBox().baseline-zeBulletTextBox().font*.65-3)/zeBulletTextBox().lineHeight)+1)')
 p.evaluate('zeSetVideoDuration(Math.ceil(zeParagraphSchedule().requiredEnd)+2)')
 assert p.evaluate('zeParagraphRenderLines(c,DURATION,zeBulletTextBox()).some(l=>l.rowId===zeParagraphSchedule().rows.at(-1).id&&l.alpha>.9)')
 print('Auto/blank grouping, measured safe capacity, matching manual holds and persistent final page: passed')

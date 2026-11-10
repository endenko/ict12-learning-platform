"""Executable checks supplement the documented human/textbook semantic sample."""
import json,sqlite3
from pathlib import Path
mcq={q['id']:q for q in json.loads(Path('lib/mcq.json').read_text())}
tf={q['id']:q for q in json.loads(Path('lib/tf.json').read_text())}
checks=[]
assert len([3,5,7])==3
assert sum(i*i for i in range(1,4))==14
assert [3,5,7][1]==5
assert sum(x%2==0 for x in [2,5,8,9,10])==3
for qid,expected in [('ext-found-q1','len'),('ext-found-q2','for'),('ext-found-q3','14'),('ext-found-q4','5'),('ext-found-q6','3')]:
 q=mcq[qid];assert expected in q['options'][q['answer']]
checks.append('Python prerequisite len, iteration, range-exclusive sum-of-squares, zero-based indexing and even counter executed')
c=sqlite3.connect(':memory:');c.execute('pragma foreign_keys=on')
c.executescript('create table HS(MaHS text primary key,HoTen text,Lop text,Diem real);insert into HS values("A","An","12A",8),("B","Binh","12A",6),("C","Chi","12B",9);')
assert [x[0] for x in c.execute('select MaHS from HS where Diem>=8 order by MaHS')]==['A','C']
q=mcq['ext-found-q12'];assert q['options'][q['answer']]=='SELECT * FROM HS WHERE Diem>=8.'
c.executescript('create table DANGKI(MaTV text not null,MaHD text not null,primary key(MaTV,MaHD));insert into DANGKI values("A","H1"),("A","H2");')
try:c.execute('insert into DANGKI values("A","H1")');raise AssertionError('duplicate composite key accepted')
except sqlite3.IntegrityError:pass
assert tf['ext-found-t2']['statements'][3]['answer'] is True
c.executescript('create table BANDOC(MaBD text primary key,Lop text);create table MUON(MaMuon text primary key,MaBD text references BANDOC(MaBD));insert into BANDOC values("A","12A"),("B","12B");insert into MUON values("M1","A"),("M2","A"),("M3","B");')
assert c.execute('select b.Lop,count(*) from BANDOC b join MUON m on m.MaBD=b.MaBD group by b.Lop order by b.Lop').fetchall()==[('12A',2),('12B',1)]
try:c.execute('delete from BANDOC where MaBD="A"');raise AssertionError('orphan allowed')
except sqlite3.IntegrityError:pass
c.executescript('create table CHITIET(SoLuong integer,DonGia real);insert into CHITIET values(2,10),(3,20);')
assert c.execute('select sum(SoLuong*DonGia) from CHITIET').fetchone()[0]==80
checks.append('SQLite predicates, composite unique/non-null key, foreign-key orphan rejection, class join/count and revenue multiplication executed')
Path('tests/readiness-semantics-results.json').write_text(json.dumps({'success':True,'checks':checks},ensure_ascii=False,indent=2))
print('\n'.join(checks))

create or replace view Q4_1(year_,sess,num)
as
select  t.year ,t.sess,count(p1.student)
from Terms t
    join ProgramEnrolments p1 on (t.id = p1.term)
    join Students s1 on (p1.student = s1.id)
where
    t.sess != 'X1'
    and t.sess != 'X2'
    and s1.stype = 'intl'
    and t.year >2004
group by t.sess
;

create or replace view Q4_2(year_ ,sess,num)
as
select t.year ,t.sess,count(p2.student)
from Terms t
    join ProgramEnrolments p2 on (t.id = p2.term)
    join Students s2 on (p2.student = s2.id)
where
    t.sess != 'X1'
    and t.sess != 'X2'
    and s2.stype = 'intl'
    or  s2.stype ='local'
    and t.year >2004
group by t.sess
;

create or replace view Q4(term, percent)
as
select substring(cast(year_ as varchar),3,2)||LOWER(sess) , Q4_1.num/Q4_2.num :: numeric(4,2)
from Q4_1
    join Q4_2 on (Q4_1.sess = Q4_2.sess)
group by sess
;


create or replace view Q4_11(student,term)
as
select p.student , p.term
from ProgramEnrolments p
     join Terms t on (p.term = t.id)
where   t.year >2004
    and t.sess != 'X1'
    and t.sess != 'X2'
;

create or replace view Q4_012(intl,term)
as
select count(*), term
from Q4_11
     join Students s on (Q4_11.student = s.id)
where s.stype = 'intl'
group by term
;

create or replace view Q4_013(total,term)
as
select count(*), term
from Q4_11
    join Students s on (Q4_11.student = s.id)
group by term
;

create or replace view Q4_014(term,id)
as
select q3(term)as term , term from Q4_012
;

create or replace view Q4(term, percent)
as
select q.term , (q1.intl/q2.total):: numeric(4,2)
from Q4_014 q
     join Q4_012 q1 on (q.id = q1.term)
     join Q4_013 q2 on (q.id = q2.term)
order by q.term
;




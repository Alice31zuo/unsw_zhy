create or replace function
   Q3(num integer) returns text
as
$$
select substring(cast(t.year as varchar),3,2)||LOWER(t.sess) from Terms t
where num = t.id
$$ language sql;

create or replace view Q4_11(student,term)
as
select p.student , p.term
from ProgramEnrolments p,Terms t
where p.term = t.id
    and t.year >2004
    and t.sess != 'X1'
    and t.sess != 'X2'
;

create or replace view Q4_012(intl,term)
as
select count(*), term
from Q4_11, Students s
where Q4_11.student = s.id
    and s.stype = 'intl'
group by term
;

create or replace view Q4_013(total,term)
as
select count(*), term
from Q4_11, Students s
where Q4_11.student = s.id
group by term
;

create or replace view Q4_014(term,id)
as
select q3(term)as term , term from Q4_12
;

create or replace view Q4(term,percent)
as
select q.term , q1.intl/q2.total :: numeric(10,2)
from Q4_014 q
     join Q4_012 q1 on (q.id = q1.term)
     join Q4_013 q2 on (q.id = q2.term)
order by q.term
;
create or replace view Q5_0(term,id)
as
select q3(t.id)as term , t.id from Terms t
where  2011 > t.year
    and  t.year > 1999
    and t.sess != 'X1'
    and t.sess != 'X2'
;

create or replace view Q5_1(cid,term,uoc)
as
select co.id, co.term , su.uoc
from Courses co
     join Subjects su on (co.subject = su.id)
     join Q5_0 q on (co.term = q.id)
;


create or replace view Q5_2(term,student,uoc)
as
select q.term , ce.student , q.uoc
from CourseEnrolments ce
     join Q5_1 q on (ce.course = q.cid)
;

create or replace view Q5(term, nstudes, fte)
as
select q1.term, count(distinct q2.student), (sum(q2.uoc)::float/24::float):: numeric(6,1)
from Q5_0 q1
    join Q5_2 q2 on (q1.id= q2.term)
group by q1.term
;


create or replace view Q6_1(sub, subject)
as
select su.id , su.code||' '||su.name
from Subjects su
    join Courses co on (co.subject = su.id)
    left join CourseStaff cs on (co.id = cs.course)
where ce.course is null
;

create or replace view Q6_2(sub, times)
as
select  q.sub ,count(q.sub)
from Q6_1 q
group by q.sub
;

create or replace view Q6(subject, nOfferings)
as
select q1.subject ,q2.times
from Q6_1 q1
    join Q6_2 q2 on (q1.sub = q2.sub)
where q2.times >30
;

////////////////////////////////////////////////
create or replace view Q6_1(sub, subject)
as
select su.id , su.code||' '||su.name
from Subjects su
    join Courses co on (co.subject = su.id)
    left join CourseStaff cs on (co.id = cs.course)
where cs.course is null
;

create or replace view Q6_2(sub, times)
as
select  q.sub ,count(q.sub)
from Q6_1 q
group by q.sub
;

create or replace view Q6(subject, nOfferings)
as
select distinct q1.subject ,q2.times
from Q6_1 q1
    join Q6_2 q2 on (q1.sub = q2.sub)
where q2.times >30
;


///////////////////////////////////////////////
create or replace view Q6_1(nocourse , sub ,countc)
as
select co.id , count(co.id)
from Courses co on
    left join CourseStaff cs on (co.id = cs.course)
where cs.course is null

;

create or replace view Q6_2(nocourse,countc)
as
select q6_1.nocourse,  q6_1.countc
from  q6_1
where q6_1.countc > 30
;



create or replace view Q6(subject, nOfferings)
as
select su.code||' '||su.name ,Q6_2
from Q6_2
    join courses co on (Q6_2.nocourse = co.id)
    join subject su on (co.subject = su.id)
;
/////////////////////////////////

create or replace view Q6_1(sub, cid, subject)
as
select su.id , co.id ,su.code||' '||su.name
from Subjects su
    join Courses co on (co.subject = su.id)
    left join CourseStaff cs on (co.id = cs.course)
where cs.course is null
;

create or replace view Q6_2(sub,times)
as
select  q.sub ,count(q.sub)
from Q6_1 q
group by q.sub
;

create or replace view Q6_3(sub, times)
as
select  q2.sub , q2.times
from Q6_2 q2
where q2.times  >30
;

create or replace view Q6(subject, nOfferings)
as
select q1.subject ,q2.times
from Q6_3 q2
    join Q6_1 q1 on (q1.sub = q2.sub)
;


/////////////////////////////////////////////////////////
create or replace view Q6_10(cid,sub)
as
select co.id, co.subject
from Courses co
    left join CourseStaff cs on (co.id = cs.course)
where cs.course is null
;


create or replace view Q6_20(subname,sub)
as
select su.code||' '||su.name , distinct su.id
from subjects su
    join Q6_10 q  on (q.sub = su.id)
;


create or replace view Q6_30(sub , time)
as
select Q6_20.sub ,count(*)
from Q6_20
group by Q6_20.sub
;

create or replace view Q6_40(sub,time)
as
select Q6_30.sub , Q6_30.time
from Q6_30
where Q6_30.time > 30
;

create or replace view Q6(subject, nOfferings)
as
select q20.subname ,q40.times
from Q6_40 q1
    join Q6_20 q2 on (q10.sub = q20.sub)
;


//////////////////////////////////////////
create or replace view Q6_10(cid,sub)         十行
as
select co.id, co.subject
from Courses co
    left join CourseStaff cs on (co.id = cs.course)
where cs.course is null
;


create or replace view Q6_20(subname,sub)
as
select su.code||' '||su.name , su.id
from subjects su
    join Q6_10 q  on (q.sub = su.id)
;

create or replace view Q6_30(sub , time)
as
select Q6_20.sub ,count(*)
from Q6_20
group by Q6_20.sub
;

create or replace view Q6_40(sub,time)
as
select Q6_30.sub , Q6_30.time
from Q6_30
where Q6_30.time > 30
;

create or replace view Q6(subject, nOfferings)
as
select distinct q2.subname ,q1.time
from Q6_40 q1
    join Q6_20 q2 on (q1.sub = q2.sub)
;

///////////////////////////////////////// 八行
create or replace view Q6_10(cid,sub)
as
select co.id, co.subject
from Courses co
    join CourseStaff cs on (co.id = cs.course)
    join subjects su on (co.subject = su.id)
;

create or replace view Q6_20(subname,sub)
as
select su.code||' '||su.name , co.subject
from subjects su
    join Courses co on (co.subject = su.id)
where co.subject not in (select Q6_10.sub from Q6_10)
;

create or replace view Q6_30(sub , time)
as
select Q6_20.sub ,count(*)
from Q6_20
group by Q6_20.sub
;

create or replace view Q6_40(sub,time)
as
select Q6_30.sub , Q6_30.time
from Q6_30
where Q6_30.time > 30
;

create or replace view Q6(subject, nOfferings)
as
select distinct q2.subname ,q1.time
from Q6_40 q1
    join Q6_20 q2 on (q1.sub = q2.sub)
;

//////////////////////////////////////////
create or replace view Q1(name, school, starting)
as
select p.name , o.longname, a.starting
from People p
    join Staffroles s on (p.id = s.id)
    join Orgunits o
    join Affiliation a
where s.description = 'Head of School'
    and a.isprimary = 't'
    and o.utype = 'School'
    and a.ending = null
    order by a.starting
;


create or replace view Q2_1_0(num)
as
select max(starting) from Q1
;

create or replace view Q2_2_0(num)
as
select min(starting) from Q1
;

create or replace view Q2_1(status, name, school, starting)
as
select 'Most recent' as status ,p.name , o.longname, a.starting from Q1
where a.starting = Q2_1_0
;

create or replace view Q2_2(status, name, school, starting)
as
select 'Longest serving' as status ,p.name , o.longname, a.starting from Q1
where a.starting = Q2_2_0
;

create or replace view Q2(status, name, school, starting)
as
select * from Q2_1 union select * from Q2_2
;

create or replace function
	Q3(num integer) returns text
as
$$
select t.year%100 ||LOWER(t.sess) from Terms t
where num = t.id
$$ language sql;

'''

create or replace view Q4_1(num)
as
select count(p1.student)
from Terms t
    join ProgramEnrolments p1
    join Students on (Students.stype = 'intl')
where t.id = p1.term
    and t.id <> ('X1','X2')
    and t.year >2004
;

create or replace view Q4_2(term, percent)
as
select count(p2.student)
from Terms t
    join ProgramEnrolments p2
where  t.id = p2.term
    and t.id <> ('X1','X2')
    and t.year >2004
;

create or replace view Q4(term, percent)
as
select q3(t.id) , cast(num1/num2)as numeric(4,2)
from Terms t ,Q4_1 ,Q4_2
;
'''


create or replace view Q4(term, percent)
as
select q3(t.id) , count(p1.student)/count(p2.student) :: numeric(4,2)
from Terms t
    join ProgramEnrolments p1
    join Students s1 on (s1.stype = 'intl',p1.student = s1.id)
    join ProgramEnrolments p2
    join Students s2 on (p2.student = s2.id)
where t.id = p1.term
    and t.id = p2.term
    and t.sess <> ('X1','X2')
    and t.year >2004
;

create or replace view Q5(term, nstudes, fte)
as
select q3(t.id), distinct ce.student, sum(su.uoc)/24 :: numeric(6,1)
from Terms t
    join Courses co on (co.term = t.id)
    join CourseEnrolments ce on (ce.course = co.id)
    join Subjects su on (co.subjucts = su.id)
where
    t.sess <> ('X1','X2'
    and 2011> t.year >1999
;

create or replace view Q6(subject, nOfferings)
as
select su.code||su.name ,count(co.courses)
from Subjects su
    join Courses co
    left join CourseStaff cs
where cs.staff is null
    and count(co.courses) >29
;

create or replace function
	Q7(var1 text) returns setof FacilityRecord
as $$
    select r.longname ,f.description
    from
    Rooms r
    join Facilities f
    join RoomFacilities rf
    where f.description like "%var1%"
$$ language sql
;


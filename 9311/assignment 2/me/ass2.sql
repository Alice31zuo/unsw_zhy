-- COMP9311 Assignment 2
-- Written by z5196480, August 2019

-- Q1: get details of the current Heads of Schools

create or replace view Q1(name, school, starting)
as
select p.name , o.longname, a.starting
from People p
    join Affiliation a on (a.staff = p.id)
    join Staffroles s on (a.role = s.id)
    join Orgunits o on (a.orgUnit = o.id)
    join OrgUnitTypes og on (o.utype = og.id)
where s.description like 'Head of School'
    and a.isprimary = 't'
    and og.name = 'School'
    and a.ending is null
    order by a.starting
;

-- Q2: longest-serving and most-recent current Heads of Schools

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
select (case
            when starting = (select num from Q2_2_0) then 'Longest serving'
            when starting = (select num from Q2_1_0) then 'Most recent'
        end)as status ,name , school, starting from Q1
;

create or replace view Q2(status, name, school, starting)
as
select * from Q2_1
where status is not null
;

-- Q3: term names

create or replace function
	Q3(num integer) returns text
as
$$
select substring(cast(t.year as varchar),3,2)||LOWER(t.sess) from Terms t
where num = t.id
$$ language sql;


-- Q4: percentage of international students, S1 and S2, 2005..2011
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
select q.term , (q1.intl :: float/q2.total :: float):: numeric(4,2)
from Q4_014 q
     join Q4_012 q1 on (q.id = q1.term)
     join Q4_013 q2 on (q.id = q2.term)
order by q.term
;

-- Q5: total FTE students per term since 2005

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

-- Q6: subjects with > 30 course offerings and no staff recorded
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

-- Q7:  which rooms have a given facility

create or replace view Q7_1
as
select r.longname ,f.description
    from
    Rooms r
    join RoomFacilities rf on rf.room = r.id
    join Facilities f on rf.facility = f.id
;

create or replace function
	Q7(var1 text) returns setof FacilityRecord
as $$
    select Q7_1.longname ,Q7_1.description
    from
    Q7_1
    where lower(Q7_1.description) like lower('%'||var1||'%')
$$ language sql
;

-- Q8: semester containing a particular day

create or replace function Q8(_day date) returns text 
as $$
declare
	... PLpgSQL variable delcarations ...
begin
	... PLpgSQL code ...
end;
$$ language plpgsql
;

-- Q9: transcript with variations

create or replace function
	q9(_sid integer) returns setof TranscriptRecord
as $$
declare
	... PLpgSQL variable delcarations ...
begin
	... PLpgSQL code ...
end;
$$ language plpgsql
;

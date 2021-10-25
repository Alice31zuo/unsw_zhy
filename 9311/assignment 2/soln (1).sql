	-- soln.sql
-- Sample solution to COMP3311 12s1 Assignment 2
-- Written by John Shepherd, April 2012


-- Q1: get details of the current Heads of Schools

create or replace view Q1(name, school, starting)
as
select p.name, u.longname, a.starting
from   People p
         join Affiliation a on (a.staff=p.id)
         join StaffRoles r on (a.role = r.id)
         join OrgUnits u on (a.orgunit = u.id)
         join OrgUnitTypes t on (u.utype = t.id)
where  r.description = 'Head of School'
         and (a.ending is null or a.ending > now()::date)
         and t.name = 'School' and a.isPrimary
;


-- Q2: longest-serving and most-recent current Heads of Schools

create or replace view LongestServingHoS(status, name, school, starting)
as
select 'Longest serving'::text, Q1.*
from   Q1
where  starting = (select min(starting) from Q1)
;

create or replace view MostRecentHoS(status, name, school, starting)
as
select 'Most recent'::text, Q1.*
from   Q1
where  starting = (select max(starting) from Q1)
;

create or replace view Q2(status, name, school, starting)
as
(select * from LongestServingHoS)
union
(select * from MostRecentHoS)
;


-- Q3: term names

create or replace function
	Q3(integer) returns text
as
$$
select substr(year::text,3,2)||lower(sess)
from   Terms
where  id = $1
$$ language sql;


-- Q4: percentage of international students, S1 and S2, 2005..2011

create or replace view EnrolmentInfo(student, stype, term)
as
select distinct pe.student, s.stype, pe.term
from   ProgramEnrolments pe
         join Students s on (pe.student = s.id)
;

create or replace view TermStats(term, nlocals, nintls, ntotal)
as
select term,
         sum(case when stype='local' then 1 else 0 end),
         sum(case when stype='intl' then 1 else 0 end),
         count(distinct student)
from   EnrolmentInfo
group  by term
;

create or replace view Q4(term, percent)
as
select q3(t.id), (nintls::float / ntotal::float)::numeric(4,2)
from   TermStats s
         join Terms t on (s.term = t.id)
where  t.sess like 'S_' and
         t.starting between '2005-01-01' and '2011-12-31'
;


-- Q5: total FTE students per term since 2005

create or replace view FTE_EnrolmentInfo(student,subject,uoc,term)
as
select e.student, s.id, s.uoc, c.term
from   CourseEnrolments e
         join Courses c on (e.course=c.id)
         join Subjects s on (c.subject=s.id)
;

create or replace view Q5(term, nstudes, fte)
as
select q3(t.id), count(distinct e.student),
        (sum(e.uoc)::float/24.0)::numeric(6,1)
from   FTE_EnrolmentInfo e
         join Terms t on (e.term = t.id)
where  t.starting between '2000-01-01' and '2010-12-31'
         and t.sess like 'S_'
group  by t.id
;


-- Q6: subjects with > 30 course offerings and no staff recorded

create or replace view Q6(subject, nOfferings)
as
select s.code||' '||s.name, count(c.id)
from   Courses c
         left outer join CourseStaff cs on (cs.course=c.id)
         join Subjects s on (c.subject = s.id)
group  by s.code,s.name
having count(cs.staff) = 0 and count(c.id) > 30
;


-- Q7:  which rooms have a given facility

create or replace function
	Q7(text) returns setof FacilityRecord
as $$
select r.longname, f.description
from   Rooms r
        join RoomFacilities rf on (rf.room=r.id)
        join Facilities f on (rf.facility=f.id)
where f.description ilike '%'||$1||'%';
-- where lower(f.description) like lower('%'||$1||'%');
$$ language sql
;


-- Q8: semester containing a particular day

create or replace function Q8(_day date) returns text 
as $$
declare
	minDate date;     -- start date of earliest semester
	maxDate date;     -- end date of last semester (in database)
	nextStart date;   -- effective start date of semester
	prevEnd date;     -- effective end date of semester
	currTerm integer; -- Terms.id of current semester
	prevTerm integer; -- Terms.id of semester before current
	nextTerm integer; -- Terms.id of semester after current
    theTerm integer;  -- matching term
	termGap interval; -- days between terms
begin
	-- check for outside range of known semesters
	select into minDate min(starting) from Terms;
	select into maxDate max(ending) from Terms;
	if (_day < minDate or _day > maxDate) then
		return null;
	end if;
	-- hande the easy case ... lies within existing semester dates
	select id into theTerm
    from   Terms
    where  _day between starting and ending;
	if (theTerm is not null) then
		return q3(theTerm);
	end if;
	-- not in a Term, find terms around given date
	select id, ending into prevTerm, prevEnd from Terms
	where  ending = (select max(ending) from Terms where ending < _day);
	select id, starting into nextTerm, nextStart from Terms
	where starting = (select min(starting) from Terms where starting > _day);
	termGap := nextStart::timestamp - prevEnd::timestamp;
	if (termGap < '1 week') then
		nextStart := (prevEnd::timestamp + '1 day')::date;
	else
		nextStart := (nextStart::timestamp - interval '1 week')::date;
		prevEnd := (nextStart::timestamp - interval '1 day')::date;
	end if;
	if (_day <= prevEnd::date) then
		return q3(prevTerm);
	elsif (_day >= nextStart::date) then
		return q3(nextTerm);
	else
		return 'Ooops?';
	end if;
end;
$$ language plpgsql
;


-- Q9: transcript with variations

create or replace function
	q9(_sid integer) returns setof TranscriptRecord
as $$
declare
	rec TranscriptRecord;
	var record;
	subj Subjects;
	UOCtotal integer := 0;
	UOCpassed integer := 0;
	UOCadvanced integer := 0;
	wsum integer := 0;
	wam integer := 0;
	stu_id integer;
begin
	select s.id into stu_id
	from   Students s join People p on (p.id=s.id)
	where  p.unswid=_sid;
	if (not found) then
		raise EXCEPTION 'Invalid student %',_sid;
	end if;
	for rec in
		select s.code, substr(t.year::text,3,2)||lower(t.sess),
			s.name, e.mark, e.grade, s.uoc
		from   CourseEnrolments e, Courses c, Subjects s, Terms t
		where  e.student = stu_id and e.course = c.id
			and c.subject = s.id and c.term = t.id
		order by t.starting,s.code
	loop
		if (rec.grade = 'SY') then
			UOCpassed := UOCpassed + rec.uoc;
		elsif (rec.mark is not null) then
			if (rec.grade in ('PT','PC','PS','CR','DN','HD')) then
				-- only counts towards creditted UOC
				-- if they passed the course
				UOCpassed := UOCpassed + rec.uoc;
			end if;
			-- we count fails towards the WAM calculation
			UOCtotal := UOCtotal + rec.uoc;
			-- weighted sum based on mark and uoc for course
			wsum := wsum + (rec.mark * rec.uoc);
		end if;
		return next rec;
	end loop;
	UOCadvanced := 0;
	for var in
		select s.id as subject, s.code, s.uoc,
		         v.vtype, v.intequiv, v.extequiv
		from   Variations v join Subjects s on (v.subject = s.id)
		where  v.student = stu_id
		order by s.code 
	loop
		-- possibilities: advstanding, substitution, exemption
		-- advstanding counts towards UOC, others don't
		rec = (var.code,null,null,null,null,null);
		if (var.vtype = 'advstanding') then
			UOCadvanced := UOCadvanced + var.uoc;
			rec.name := 'Advanced standing, based on ...';
			rec.uoc  := var.uoc;
		elsif (var.vtype = 'substitution') then
			rec.name := 'Substitution, based on ...';
		else
			rec.name := 'Exemption, based on ...';
		end if;
		return next rec;
		-- possibilities: internal/external subject
		rec.code := null; rec.uoc := null;
		if (var.intequiv is not null) then
			select 'studying '||code||' at UNSW' into rec.name
			from   Subjects where id = var.intequiv;
		else
			select 'study at '||institution into rec.name
			from   ExternalSubjects where id = var.extequiv;
		end if;
		return next rec;
	end loop;
	-- append record containing WAM
	if (UOCtotal = 0) then
		rec := (null,null,'No WAM available',null,null,null);
	else
		wam := wsum / UOCtotal;
		rec := (null,null,'Overall WAM',wam,null,UOCpassed+UOCadvanced);
	end if;
	return next rec;
end;
$$ language plpgsql
;

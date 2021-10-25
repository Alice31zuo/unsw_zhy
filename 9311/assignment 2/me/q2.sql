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


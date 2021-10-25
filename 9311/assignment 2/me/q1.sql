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
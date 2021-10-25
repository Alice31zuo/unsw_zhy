create or replace function
	Q7(var1 text) returns setof FacilityRecord
as $$
    select r.longname ,f.description
    from
    Rooms r
    join RoomFacilities rf on rf.room = r.id
    join Facilities f on rf.facility = f.id
    where f.description like "%var1%"
$$ language sql
;

////////////////////////////////////
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
declare @var varchar = cast(var1 as varchar)
begin
    select Q7_1.longname ,Q7_1.description
    from
    Q7_1
    where lower(Q7_1.description) like lower('%'+var1+'%')
end
$$ language sql
;

///////////////////////////////////////////////////////

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

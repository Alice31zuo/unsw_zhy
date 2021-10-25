create or replace function
Q3(num integer) returns text
as
$$
select substring(cast(t.year as varchar),3,2)||LOWER(t.sess) from Terms t
where num = t.id
$$ language sql;
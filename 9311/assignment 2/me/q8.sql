-- Q8: semester containing a particular day
create or replace view Q8_1
as
select row_number() over (order by starting) as row, *
    from
    Terms t
;

create or replace function Q8(_day date) returns text
as $$
declare
	@date1 date
	@date2 date
	@date3 date  = _day
	@row  integer
	set @date1 = select ending from Q8_1 where row = 1
	set @date2 = select starting from Q8_1 where row = 2
	set @row = 3
begin
    while (@date1 < @date3 and @date2 < @date3) loop
        @date1 = select ending from Q8_1 where row = (@row -1)
        @date2 = select starting from Q8_1 where row = @row
        @row = @row + 1
    end loop
    if (@date2 - @date1) > 7
    then
    if

	select  q3(Q8_1.id) from Q8_1 where Q8_1.row = (select case when @date2 - @date1 > 7 then interval(@date3,(@row - 2),(@row - 1) else then (@row - 1)))
end;
$$ language plpgsql
;

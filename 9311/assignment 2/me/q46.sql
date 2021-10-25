create or replace view Q4_1
as
select p.student , p.term
from ProgramEnrolments p,Terms t
where p.term = t.id
    and t.year >2004
    and t.sess != 'X1'
    and t.sess != 'X2'
;





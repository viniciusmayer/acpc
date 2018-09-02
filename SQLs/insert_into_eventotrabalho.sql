-- FUNCTION: public.insert_into_eventotrabalho(integer)

-- DROP FUNCTION public.insert_into_eventotrabalho(integer);

CREATE OR REPLACE FUNCTION public.insert_into_eventotrabalho(
	evento integer)
    RETURNS boolean
    LANGUAGE 'plpgsql'

    COST 100
    VOLATILE 
AS $BODY$

declare
	i integer;
	j integer;

begin
	select max(ordem) + 5 into j from trabalhos_eventotrabalho where evento_id = evento;
	for i in select t.id from trabalhos_trabalho t
			inner join trabalhos_tag ta on ta.id=t.tag_id
				and t.id not in (
					select _et.trabalho_id from trabalhos_eventotrabalho _et  where _et.evento_id = evento
				)
			inner join trabalhos_arquivo a on a.id=t.arquivo_id
		order by ta.ordem, t.ano desc, t.titulo
	loop
		insert into trabalhos_eventotrabalho (evento_id, trabalho_id, ordem) values (evento, i, j);
		j := j + 2;
	end loop;
	return True;
end;

$BODY$;

ALTER FUNCTION public.insert_into_eventotrabalho(integer)
    OWNER TO acpc;

--selecionar o evento em questão
select id from trabalhos_evento where nome = 'UEMS' and quando = '2018-09-10'

--selecionar todos os trabalhos que não estão associados ao evento em questão, na ordem para associação
select t.id
from trabalhos_trabalho t
	inner join trabalhos_tag ta on ta.id=t.tag_id
		and t.id not in (
			select _et.trabalho_id
				from trabalhos_eventotrabalho _et
					inner join trabalhos_evento _e on _e.id=_et.evento_id
						and _e.id = (select id from trabalhos_evento where nome = 'UEMS' and quando = '2018-09-10')
			
		)
	inner join trabalhos_arquivo a on a.id=t.arquivo_id
order by ta.ordem, t.ano, t.titulo

--verificar que todos os arquivos estão associados a um trabalho
select *
from trabalhos_arquivo a
where a.id not in (
	select arquivo_id from trabalhos_trabalho
)

--verificar que todos os trabalhos estão associados ao evento em questão
select *
from trabalhos_trabalho t
where t.id not in (
	select trabalho_id from trabalhos_eventotrabalho et
		inner join trabalhos_evento e on e.id=et.evento_id
			and nome = 'UEMS' and quando = '2018-09-10'
)
	and arquivo_id is not null
# acpc
academic curriculum proof copy

# setup
docker run -p 5432:5432 --name postgres -e POSTGRES_PASSWORD=p05tgr35 -d postgres
docker run -p 5050:5050 --name pgadmin4 -e "PGADMIN_DEFAULT_EMAIL=viniciusmayer@gmail.com" -e "PGADMIN_DEFAULT_PASSWORD=v1n1c1u5" -d --link postgres:postgres dpage/pgadmin4
docker run -p 15672:15672 -p 5672:5672 --name rabbitmq -d rabbitmq:3-management

# ordem lattes
Formação acadêmica/titulação                    [done] FORMACAO-ACADEMICA-TITULACAO
Formação Complementar                           [done] FORMACAO-COMPLEMENTAR-DE-EXTENSAO-UNIVERSITARIA
                                                [done] FORMACAO-COMPLEMENTAR-CURSO-DE-CURTA-DURACAO
Atuação Profissional                            [todo] ATUACOES-PROFISSIONAIS
Linhas de pesquisa                              [----]
Projetos de pesquisa                            [done] PROJETO-DE-PESQUISA
Projetos de extensão                            [done] PROJETO-DE-PESQUISA.EXTENSAO
Revisor de periódico                            [todo]
Áreas de atuação                                [----] AREAS-DE-ATUACAO
Idiomas                                         [----] IDIOMAS
Prêmios e títulos                               [done] PREMIOS-TITULOS
Produções                                       [----]
  Produção bibliográfica                        [----] PRODUCAO-BIBLIOGRAFICA
    Artigos completos publicados em periódicos  [done] ARTIGOS-PUBLICADOS
    Livros publicados/organizados ou edições    [done] LIVROS-PUBLICADOS-OU-ORGANIZADOS
    Capítulos de livros publicados              [done] CAPITULOS-DE-LIVROS-PUBLICADOS
    Trabalhos completos publicados em anais de congressos   [done] TRABALHO-EM-EVENTOS.COMPLETO
    Resumos expandidos publicados em anais de congressos    [done] TRABALHO-EM-EVENTOS.RESUMO_EXPANDIDO
    Resumos publicados em anais de congressos   [done] TRABALHO-EM-EVENTOS.RESUMO
    Apresentações de Trabalho                   [done] APRESENTACAO-DE-TRABALHO
  Produção técnica                              [----] PRODUCAO-TECNICA
    Trabalhos técnicos                          [done] TRABALHO-TECNICO
  Demais tipos de produção técnica              [done] CURSO-DE-CURTA-DURACAO-MINISTRADO
Bancas                                          [----]
  Participação em bancas de comissões julgadoras            [----]
    Outras participações                        [done] OUTRAS-BANCAS-JULGADORAS
Eventos                                         [----]
  Participação em eventos, congressos, exposições e feiras  [done] PARTICIPACAO-EM-CONGRESSO
                                                            [done] PARTICIPACAO-EM-SEMINARIO
                                                            [done] PARTICIPACAO-EM-SIMPOSIO
                                                            [done] PARTICIPACAO-EM-ENCONTRO
                                                            [done] OUTRAS-PARTICIPACOES-EM-EVENTOS-CONGRESSOS
  Organização de eventos, congressos, exposições e feiras   [todo] ORGANIZACAO-DE-EVENTO
Outras informações relevantes                   [----]

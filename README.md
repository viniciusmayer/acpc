# acpc
academic curriculum proof copy

# setup
docker run -p 5432:5432 --name postgres -e POSTGRES_PASSWORD=p05tgr35 -d postgres
docker run -p 5050:5050 --name pgadmin4 -e "PGADMIN_DEFAULT_EMAIL=viniciusmayer@gmail.com" -e "PGADMIN_DEFAULT_PASSWORD=v1n1c1u5" -d --link postgres:postgres dpage/pgadmin4
docker run -p 15672:15672 -p 5672:5672 --name rabbitmq -d rabbitmq:3-management

# ordem lattes
Formação acadêmica/titulação                    FORMACAO-ACADEMICA-TITULACAO
Formação Complementar                           FORMACAO-COMPLEMENTAR-DE-EXTENSAO-UNIVERSITARIA
                                                FORMACAO-COMPLEMENTAR-CURSO-DE-CURTA-DURACAO
Atuação Profissional                            ATUACOES-PROFISSIONAIS
Linhas de pesquisa
Projetos de pesquisa
Projetos de extensão
Revisor de periódico
Áreas de atuação                                AREAS-DE-ATUACAO
Idiomas                                         IDIOMAS
Prêmios e títulos                               PREMIOS-TITULOS
Produções
  Produção bibliográfica                        PRODUCAO-BIBLIOGRAFICA
    Artigos completos publicados em periódicos  ARTIGOS-PUBLICADOS
    Livros publicados/organizados ou edições    LIVROS-PUBLICADOS-OU-ORGANIZADOS
    Capítulos de livros publicados              CAPITULOS-DE-LIVROS-PUBLICADOS
    Trabalhos completos publicados em anais de congressos
    Resumos expandidos publicados em anais de congressos
    Resumos publicados em anais de congressos
    Apresentações de Trabalho
  Produção técnica                              PRODUCAO-TECNICA
    Trabalhos técnicos                          TRABALHO-TECNICO
  Demais tipos de produção técnica              APRESENTACAO-DE-TRABALHO
                                                CURSO-DE-CURTA-DURACAO-MINISTRADO
                                                ORGANIZACAO-DE-EVENTO
Bancas
  Participação em bancas de comissões julgadoras
    Outras participações                        OUTRAS-BANCAS-JULGADORAS
Eventos
  Participação em eventos, congressos, exposições e feiras
  Organização de eventos, congressos, exposições e feiras
Outras informações relevantes

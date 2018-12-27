import csv
from xml.dom import minidom

import psycopg2


class ImportarLattesService(object):
    
    def __init__(self, lattes, armazenamento):
        self.connection = None
        self.cursor = None
        self.nomeArquivoDestino = None
        csv.register_dialect('myDialect', delimiter = ';', quotechar = '"', quoting=csv.QUOTE_ALL, skipinitialspace=True)
        if (armazenamento == 'DATABASE'):
            self.connection = psycopg2.connect("dbname='acpc' user='acpc' host='localhost' password='v1n1c1u5'")
            self.cursor = self.connection.cursor()
        elif (armazenamento == 'FILE'):
            self.nomeArquivoDestino = 'lattesitens.csv'
            with open(self.nomeArquivoDestino, mode='w', newline='') as arquivoDestino:
                writer = csv.writer(arquivoDestino, dialect='myDialect')
                writer.writerow(['titulo', 'ano', 'anoFim', 'natureza', 'entidade', 'tag'])
                arquivoDestino.close()
        self.arquivo = minidom.parse(lattes)

    def inserirEntidade(self, nome):
        descricao = nome
        nome = self.tratarEntidade(nome)
        select = 'SELECT id FROM public.trabalhos_entidade where nome = \'{n}\''.format(n=nome)
        self.cursor.execute(select)
        if (self.cursor.rowcount == 0):
            insert = 'INSERT INTO public.trabalhos_entidade(nome, descricao, ativo) VALUES (\'{n}\', \'{d}\', true);'.format(n=nome, d=descricao)
            self.cursor.execute(insert)
            self.connection.commit()
            print('entidade inserida: {n}'.format(n=nome))
        else:
            print('entidade ignorada: {n}'.format(n=nome))
        return nome

    def inserirTag(self, nome, ordem):
        descricao = nome
        nome = nome.replace('-', ' ').strip().title()
        select = 'select id from public.trabalhos_tag where nome = \'{0}\''.format(nome)
        self.cursor.execute(select)
        if (self.cursor.rowcount == 0):
            insert = 'insert into public.trabalhos_tag(nome, descricao, ordem, ativo) values (\'{n}\', \'{d}\', {o}, true)'.format(n=nome
                                                                                                                      , d=descricao
                                                                                                                      , o=ordem)
            self.cursor.execute(insert)
            self.connection.commit()
            print('tag inserido: {0}, {1}'.format(nome, ordem))
        else:
            print('tag ignorado: {0}, {1}'.format(nome, ordem))        
        return nome
        
    def inserirNatureza(self, nome):
        descricao = nome
        nome = nome.replace('-', ' ').strip().title()
        select = 'select id from public.trabalhos_natureza where nome = \'{0}\''.format(nome)
        self.cursor.execute(select)
        if (self.cursor.rowcount == 0):
            insert = 'insert into public.trabalhos_natureza(nome, descricao, ativo) values (\'{n}\', \'{d}\', true)'.format(n=nome, d=descricao)
            self.cursor.execute(insert)
            self.connection.commit()
            print('natureza inserido: {0}'.format(nome))
        else:
            print('natureza ignorado: {0}'.format(nome))
        return nome
            
    def inserirTrabalho(self, titulo, ano, anoFim, natureza, entidade, tag):
        selectTag = 'select id from public.trabalhos_tag where nome = \'{n}\''.format(n=tag)
        selectNatureza = 'select id from public.trabalhos_natureza where nome = \'{n}\''.format(n=natureza)
        selectEntidade = 'SELECT id FROM public.trabalhos_entidade where nome = \'{n}\''.format(n=entidade)
        select = 'SELECT t.id FROM public.trabalhos_trabalho t \
                    inner join public.trabalhos_natureza n on n.id=t.natureza_id \
                        and t.ano = {a} and t.titulo = \'{t}\' and n.nome = \'{n}\' \
                    inner join public.trabalhos_tag ta on ta.id=t.tag_id \
                        and ta.nome = \'{ta}\''.format(a=ano, t=titulo, n=natureza, ta=tag)
        self.cursor.execute(select)
        if (self.cursor.rowcount == 0):
            insert = 'INSERT INTO public.trabalhos_trabalho(ano, titulo, ano_fim, tag_id, natureza_id, entidade_id, ativo) \
                        VALUES ({a}, \'{t}\', {af}, ({ta}), ({na}), ({e}), true);'.format(a=ano, t=titulo, af='null' if not anoFim else anoFim
                                                                          , ta=selectTag.format(tag)
                                                                          , na=selectNatureza.format(natureza)
                                                                          , e=selectEntidade.format(entidade))
            self.cursor.execute(insert)
            self.connection.commit()
            print('trabalho inserido: {0}, {1}, {2}, {3}, {4}, {5}'.format(titulo, ano, anoFim, natureza, entidade, tag))
        else:
            print('trabalho ignorado: {0}, {1}, {2}, {3}, {4}, {5}'.format(titulo, ano, anoFim, natureza, entidade, tag))                

    def extrairDados(self, elemento, ano, anoTag
                     , anoFim, anoFimTag
                     , titulo, tituloTag
                     , natureza, naturezaTag
                     , entidade, entidadeTagName):
        _ano = elemento.getAttribute(anoTag).strip()
        ano = _ano if _ano else ano
        _anoFim = ano if not anoFimTag else elemento.getAttribute(anoFimTag).strip()
        anoFim = _anoFim if _anoFim else anoFim
        _titulo = elemento.getAttribute(tituloTag).strip()
        titulo = _titulo if _titulo else titulo
        _natureza = elemento.getAttribute(naturezaTag).strip()
        natureza = _natureza if _natureza else natureza 
        natureza = 'OUTRA' if not natureza or natureza == 'NAO_INFORMADO' else natureza.replace('_', ' ').replace('ó', 'o')
        _entidade = elemento.getAttribute(entidadeTagName).strip() if entidadeTagName else None
        entidade = _entidade if _entidade else entidade
        return ano, anoFim, titulo, natureza, entidade
    
    def tratarHifen(self, caracter, entidade):
        a = entidade.find(caracter)
        if a > 0:
            b = len(entidade) - (a + 2)
            if a > b: entidade = entidade[(a + 2):len(entidade)]
            else: entidade = entidade[0:a]
        return entidade

    def tratarDoisPontos(self, caracter, entidade):
        a = entidade.find(caracter)
        if a > 0: entidade = entidade[0:a]
        return entidade
    
    def tratarVirgula(self, caracter, entidade):
        a = entidade.find(caracter)
        if a > 0: entidade = entidade[(a+2):len(entidade)]
        return entidade
    
    def tratarEntidade(self, entidade):
        if entidade:
            entidade = entidade.replace('Universidade Federal do Rio Grande do Sul', 'UFRGS')
            entidade = entidade.replace('Universidade Federal do Rio Grande Sul', 'UFRGS')
            entidade = entidade.replace('Universidade Federal do Rio Grande', 'FURG')
            entidade = entidade.replace('Universidade Regional do Noroeste do Estado do Rio Grande do Sul', 'UNIJUI')
            entidade = entidade.replace('Instituto Federal de Educação, Ciência e Tecnologia do Rio Grande do Sul', 'IFRS')
            entidade = entidade.replace('Universidade Federal do Mato Grosso do Sul', 'UFMS')
            entidade = entidade.replace('Centro Universitário Ritter dos Reis', 'UniRitter')
            entidade = entidade.replace('Universidade Federal de Pernambuco', 'UFPE')
            entidade = entidade.replace('Universidade Federal do Pampa', 'Unipampa')
            entidade = entidade.replace('Serviço Nacional de Aprendizagem Comercial do Rio Grande do Sul', 'SENAC')
            entidade = entidade.replace('Universidade de Caxias do Sul', 'UCS')
            entidade = entidade.replace('í', 'i')
            entidade = entidade.replace('BlueSky', 'Blue Sky')
            entidade = entidade.replace('Seminário de Estudos em Análise do Discurso', 'SEAD')
            entidade = entidade.replace('UCPEL', 'UCPel')
            entidade = entidade.replace('Unijui', 'UNIJUI')
            entidade = entidade.replace('.', '')
            entidade = self.tratarHifen(' - ', entidade)
            entidade = self.tratarDoisPontos(': ', entidade)
            entidade = self.tratarVirgula(', ', entidade)
            entidade = entidade.strip()
        return entidade

    def inserir(self, titulo, ano, anoFim, natureza, entidade, tagName, tagOrdem):
        if (self.connection is not None and self.cursor is not None):
            tagName = self.inserirTag(tagName, tagOrdem)
            natureza = self.inserirNatureza(natureza)
            if entidade: entidade = self.inserirEntidade(entidade)
            self.inserirTrabalho(titulo, ano, anoFim, natureza, entidade, tagName)
        elif (self.nomeArquivoDestino is not None):
            with open(self.nomeArquivoDestino, mode='a', newline='') as arquivoDestino:
                writer = csv.writer(arquivoDestino, dialect='myDialect')
                writer.writerow([titulo, ano, anoFim, natureza, entidade, tagName])
                arquivoDestino.close()

    def processar(self, tagName, tagOrdem=None
                  , dadosBasicosTagName=None
                  , tituloAttributeName='TITULO'
                  , anoAttributeName='ANO' 
                  , anoFimAttributeName=None
                  , naturezaAttributeName='NATUREZA'
                  , detalhamentoTagName=None
                  , nomeDoEventoAttributeName='NOME-DO-EVENTO'
                  , entidadeTagName='NOME-INSTITUICAO'):
        elementos = self.arquivo.getElementsByTagName(tagName)
        for elemento in elementos:
            _elemento = elemento
            ano, anoFim, titulo, natureza, entidade = None, None, None, None, None
            ano, anoFim, titulo, natureza, entidade = self.extrairDados(_elemento, ano, anoAttributeName
                                                                        , anoFim, anoFimAttributeName
                                                                        , titulo, tituloAttributeName
                                                                        , natureza, naturezaAttributeName
                                                                        , entidade, entidadeTagName)
            
            if dadosBasicosTagName:
                _elemento = elemento.getElementsByTagName(dadosBasicosTagName)[0]
                ano, anoFim, titulo, natureza, entidade = self.extrairDados(_elemento, ano, anoAttributeName
                                                                            , anoFim, anoFimAttributeName
                                                                            , titulo, tituloAttributeName
                                                                            , natureza, naturezaAttributeName
                                                                            , entidade, entidadeTagName)
                
            if detalhamentoTagName and len(elemento.getElementsByTagName(detalhamentoTagName)) > 0:
                for _elemento in elemento.getElementsByTagName(detalhamentoTagName):
                    ano, anoFim, titulo, natureza, entidade = self.extrairDados(_elemento, ano, anoAttributeName
                                                                                , anoFim, anoFimAttributeName
                                                                                , titulo, nomeDoEventoAttributeName
                                                                                , natureza, naturezaAttributeName
                                                                                , entidade, entidadeTagName)
                    self.inserir(titulo, ano, anoFim, natureza, entidade, tagName, tagOrdem)
            else:
                self.inserir(titulo, ano, anoFim, natureza, entidade, tagName, tagOrdem)

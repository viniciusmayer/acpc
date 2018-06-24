from xml.dom import minidom

import psycopg2


class ImportarLattesService(object):
    
    def __init__(self, lattes):
        self.conn = psycopg2.connect("dbname='acpc' user='acpc' host='localhost' password='v1n1c1u5'")
        self.cursor = self.conn.cursor()
        self.arquivo = minidom.parse(lattes)

    def inserirTag(self, nome, ordem):
        select = 'select id from public.trabalhos_tag where nome = \'{0}\''.format(nome)
        self.cursor.execute(select)
        if (self.cursor.rowcount == 0):
            insert = 'insert into public.trabalhos_tag(nome, ordem) values (\'{0}\', {1})'.format(nome, ordem)
            self.cursor.execute(insert)
            self.conn.commit()
            print('tag inserido: {0}, {1}'.format(nome, ordem))
        else:
            print('tag ignorado: {0}, {1}'.format(nome, ordem))        
        
    def inserirNatureza(self, nome):
        select = 'select id from public.trabalhos_natureza where nome = \'{0}\''.format(nome)
        self.cursor.execute(select)
        if (self.cursor.rowcount == 0):
            insert = 'insert into public.trabalhos_natureza(nome) values (\'{0}\')'.format(nome)
            self.cursor.execute(insert)
            self.conn.commit()
            print('natureza inserido: {0}'.format(nome))
        else:
            print('natureza ignorado: {0}'.format(nome))
        return nome
            
    def inserirTrabalho(self, titulo, ano, anoFim, natureza, tag):
        selectTag = 'select id from public.trabalhos_tag where nome = \'{0}\''.format(tag)
        selectNatureza = 'select id from public.trabalhos_natureza where nome = \'{0}\''.format(natureza)
        select = 'SELECT t.id FROM public.trabalhos_trabalho t \
                    inner join public.trabalhos_natureza n on n.id=t.natureza_id \
                        and t.ano = {0} and t.titulo = \'{1}\' and n.nome = \'{2}\' \
                    inner join public.trabalhos_tag ta on ta.id=t.tag_id \
                        and ta.nome = \'{3}\''.format(ano, titulo, natureza, tag)
        self.cursor.execute(select)
        if (self.cursor.rowcount == 0):
            insert = 'INSERT INTO public.trabalhos_trabalho(ano, titulo, ano_fim, tag_id, natureza_id) \
                        VALUES ({0}, \'{1}\', {2}, ({3}), ({4}));'.format(ano, titulo, 'null' if not anoFim else anoFim
                                                                          , selectTag.format(tag)
                                                                          , selectNatureza.format(natureza))
            self.cursor.execute(insert)
            self.conn.commit()
            print('trabalho inserido: {0}, {1}, {2}, {3}, {4}'.format(titulo, ano, anoFim, natureza, tag))
        else:
            print('trabalho ignorado: {0}, {1}, {2}, {3}, {4}'.format(titulo, ano, anoFim, natureza, tag))                

    def setValues(self, elemento, ano, anoTag, anoFim, anoFimTag, titulo, tituloTag, natureza, naturezaTag):
        _ano = elemento.getAttribute(anoTag).strip()
        ano = _ano if _ano else ano
        _anoFim = ano if not anoFimTag else elemento.getAttribute(anoFimTag).strip()
        anoFim = _anoFim if _anoFim else anoFim
        _titulo = elemento.getAttribute(tituloTag).strip()
        titulo = _titulo if _titulo else titulo
        _natureza = elemento.getAttribute(naturezaTag).strip()
        natureza = _natureza if _natureza else natureza 
        natureza = 'OUTRA' if not natureza or natureza== 'NAO_INFORMADO' else natureza.upper().replace(' ', '-').replace('_', '-').replace('Ó', 'O').replace('Á', 'A')
        return ano, anoFim, titulo, natureza

    def processar(self, tagName, tagOrdem=None, dadosBasicosTagName=None, tituloAttributeName='TITULO', anoAttributeName='ANO'
                  , anoFimAttributeName=None, naturezaAttributeName='NATUREZA', detalhamentoTagName=None, nomeDoEventoAttributeName='NOME-DO-EVENTO'):
        self.inserirTag(tagName, tagOrdem)
        elementos = self.arquivo.getElementsByTagName(tagName)
        for elemento in elementos:
            _elemento = elemento
            if dadosBasicosTagName:
                _elemento = elemento.getElementsByTagName(dadosBasicosTagName)[0]
            ano, anoFim, titulo, natureza = [None, None, None, None]
            ano, anoFim, titulo, natureza = self.setValues(_elemento, ano, anoAttributeName, anoFim, anoFimAttributeName, titulo, tituloAttributeName, natureza, naturezaAttributeName)
            if detalhamentoTagName and len(elemento.getElementsByTagName(detalhamentoTagName)) > 0:
                for _elemento in elemento.getElementsByTagName(detalhamentoTagName):
                    ano, anoFim, titulo, natureza = self.setValues(_elemento, ano, anoAttributeName, anoFim, anoFimAttributeName, titulo, nomeDoEventoAttributeName, natureza, naturezaAttributeName)
                    self.inserirNatureza(natureza)
                    self.inserirTrabalho(titulo, ano, anoFim, natureza, tagName)
            else:
                self.inserirNatureza(natureza)
                self.inserirTrabalho(titulo, ano, anoFim, natureza, tagName)

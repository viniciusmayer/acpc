from xml.dom import minidom

import psycopg2


class ImportarLattesService(object):
    
    def __init__(self, lattes):
        self.conn = psycopg2.connect("dbname='acpc' user='acpc' host='localhost' password='v1n1c1u5'")
        self.cursor = self.conn.cursor()
        self.arquivo = minidom.parse(lattes)
        
    def processar(self, tagName
                  , dadosBasicosTagName=None
                  , tituloAttributeName='TITULO'
                  , anoAttributeName='ANO'
                  , anoFimAttributeName=None
                  , naturezaAttributeName='NATUREZA'
                  , detalhamentoTagName=None
                  , nomeDoEventoAttributeName='NOME-DO-EVENTO'):
        elementos = self.arquivo.getElementsByTagName(tagName)
        for elemento in elementos:
            ano = None
            anoFim = None
            titulo = None
            natureza = None
            
            _elemento = elemento
            if dadosBasicosTagName:
                _elemento = elemento.getElementsByTagName(dadosBasicosTagName)[0]
            ano = _elemento.getAttribute(anoAttributeName).strip()
            anoFim = ano if not anoFimAttributeName else _elemento.getAttribute(anoFimAttributeName).strip()  
            titulo = _elemento.getAttribute(tituloAttributeName).strip()
            natureza = _elemento.getAttribute(naturezaAttributeName).strip()

            if len(elemento.getElementsByTagName(detalhamentoTagName)) > 0:
                _elemento = elemento.getElementsByTagName(detalhamentoTagName)[0] 
                if not ano:
                    ano = _elemento.getAttribute(anoAttributeName).strip()
                if not anoFim:
                    anoFim = ano if not anoFimAttributeName else _elemento.getAttribute(anoFimAttributeName).strip() 
                if not titulo:
                    titulo = _elemento.getAttribute(nomeDoEventoAttributeName).strip()
                if not natureza:
                    natureza = _elemento.getAttribute(naturezaAttributeName).strip()

            natureza = 'OUTRA' if not natureza or natureza == 'NAO_INFORMADO' else natureza.upper().replace(' ', '-').replace('_', '-')
            natureza = 'SIMPOSIO' if natureza == 'SIMPÓSIO' else natureza
            
            select = 'select id from public.trabalhos_trabalho \
                        where titulo = \'{0}\' and ano = {1} and natureza = \'{2}\' and tag = \'{3}\''.format(titulo, ano, natureza, tagName)
            self.cursor.execute(select)
            if (self.cursor.rowcount == 0):
                insert = 'insert into public.trabalhos_trabalho (titulo, ano, natureza, tag, ano_fim) \
                            values (\'{0}\', {1}, \'{2}\', \'{3}\', {4})'.format(titulo, ano, natureza, tagName, 'null' if not anoFim else anoFim)
                self.cursor.execute(insert)
                self.conn.commit()
                print('trabalho inserido: {0}, {1}, {2}, {3}, {4}'.format(titulo, ano, natureza, tagName, anoFim))
            else:
                print('trabalho ignorado: {0}, {1}, {2}, {3}, {4}'.format(titulo, ano, natureza, tagName, anoFim))
import psycopg2


class ImportarLattesService(object):
    
    def __init__(self, arquivoXML):
        self.conn = psycopg2.connect("dbname='acpc' user='acpc' host='localhost' password='v1n1c1u5'")
        self.cursor = self.conn.cursor()
        self.arquivoXML = arquivoXML
        
    def processar(self, tagName, dadosBasicosTagName, tituloAttributeName='TITULO', anoAttributeName='ANO', naturezaAttributeName='NATUREZA', detalhamentoTagName=None, nomeDoEventoAttributeName='NOME-DO-EVENTO'):
        elementos = self.arquivoXML.getElementsByTagName(tagName)
        for elemento in elementos:
            dadosBasicos = elemento.getElementsByTagName(dadosBasicosTagName)
            ano = dadosBasicos[0].getAttribute(anoAttributeName)
            titulo = dadosBasicos[0].getAttribute(tituloAttributeName)
            natureza = dadosBasicos[0].getAttribute(naturezaAttributeName)
            if not titulo.strip():
                detalhamento = elemento.getElementsByTagName(detalhamentoTagName)
                titulo = detalhamento[0].getAttribute(nomeDoEventoAttributeName)
            select = 'select id from trabalhos_trabalho where titulo = \'{0}\' and ano = {1} and natureza = \'{2}\''.format(titulo, ano, natureza)
            self.cursor.execute(select)
            if (self.cursor.rowcount == 0):
                insert = 'insert into trabalhos_trabalho (titulo, ano, natureza) values (\'{0}\', {1}, \'{2}\')'.format(titulo, ano, natureza)
                self.cursor.execute(insert)
                print('trabalho inserted: {0}, {1}, {2}'.format(titulo, ano, natureza))
                self.conn.commit()
            else:
                print('trabalho NOT inserted: {0}, {1}, {2}'.format(titulo, ano, natureza))
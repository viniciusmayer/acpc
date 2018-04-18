from acpa.Entity import Trabalho
import sqlite3

class Processar(object):
    
    def __init__(self, arquivoXML):
        self.conn = sqlite3.connect('lattes.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('create table if not exists trabalho(id INTEGER PRIMARY KEY, titulo TEXT, ano INTEGER, natureza TEXT)')
        self.conn.commit()
        self.arquivoXML = arquivoXML
        self.trabalhos = []
        self.contador = 0
        
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
            self.trabalhos.append(Trabalho(self.proximoNumero(), ano, titulo, natureza))
            insert = 'insert into trabalho (titulo, ano, natureza) values ({0}, {1}, {2})'
            insert = insert.format(titulo, ano, natureza)
            self.cursor.execute(insert)
            self.cursor.commit()

    def imprimir(self):
        for trabalho in self.trabalhos:
            trabalho.imprimir()
            
    def imprimirDb(self):
        self.cursor.execute('select id, titulo, ano, natureza from trabalho')
        for linha in self.cursor.fetchall():
            t = Trabalho(linha[0], linha[2], linha[1], linha[3])
            t.imprimir()
            
    def proximoNumero(self):
        self.contador += 1
        return self.contador

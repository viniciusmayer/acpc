from acpa.Entity import Trabalho

class Processar(object):
    
    def __init__(self, arquivoXML):
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

    def imprimir(self):
        for trabalho in self.trabalhos:
            trabalho.imprimir()
            
    def proximoNumero(self):
        self.contador += 1
        return self.contador
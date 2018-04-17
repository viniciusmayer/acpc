from PyPDF2 import PdfFileWriter, PdfFileReader
import os

class PDFService(object):

    def __init__(self, cabecalho, pastaOrigem, destino):
        self.cabecalho = PdfFileReader(open(cabecalho, 'rb'))

        arquivos = [x for x in os.listdir(pastaOrigem) if x.endswith('.pdf')]
        self.arquivosOrigem = [] 
        for arquivo in sorted(arquivos):
            self.arquivosOrigem.append(
                PdfFileReader(open('{0}{1}'.format(pastaOrigem, arquivo), 'rb')))
        
        self.nomeArquivoDestino = destino
        self.arquivoDestino = PdfFileWriter()

    def processar(self):            
        contadorCabecalho = 0
        for i in self.arquivosOrigem:
            for j in range(i.getNumPages()):
                cabecalho = self.cabecalho.getPage(contadorCabecalho)
                contadorCabecalho += 1
                pagina = i.getPage(j)
                pagina.mergePage(cabecalho)
                self.arquivoDestino.addPage(pagina)
        
        with open(self.nomeArquivoDestino, 'wb') as f:
           self.arquivoDestino.write(f)
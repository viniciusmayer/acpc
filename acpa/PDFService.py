from PyPDF2 import PdfFileWriter, PdfFileReader
import glob

class PDFService(object):

    def __init__(self, cabecalho, pastaOrigem, destino):
        self.cabecalho = PdfFileReader(open(cabecalho, 'rb'))
        self.arquivosOrigem = [] 
        for arquivo in glob.iglob(pastaOrigem + '**/*.pdf', recursive=True):
            self.arquivosOrigem.append(PdfFileReader(open(arquivo, 'rb')))
        self.nomeArquivoDestino = destino
        self.arquivoDestino = PdfFileWriter()

    def processar(self):            
        contadorCabecalho = -1
        for i in self.arquivosOrigem:
            for j in range(i.getNumPages()):
                contadorCabecalho += 1
                cabecalho = self.cabecalho.getPage(contadorCabecalho)
                pagina = i.getPage(j)
                pagina.mergePage(cabecalho)
                self.arquivoDestino.addPage(pagina)
        
        with open(self.nomeArquivoDestino, 'wb') as f:
            self.arquivoDestino.write(f)

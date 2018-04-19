from PyPDF2 import PdfFileWriter, PdfFileReader
import glob

class PDFService(object):

    def __init__(self, pastaOrigem, destino):
        self.arquivosOrigem = [] 
        for arquivo in glob.iglob(pastaOrigem + '**/*.pdf', recursive=True):
            self.arquivosOrigem.append(PdfFileReader(open(arquivo, 'rb')))
        self.nomeArquivoDestino = destino
        self.arquivoDestino = PdfFileWriter()

    def processar(self, cabecalho):            
        cabecalho = PdfFileReader(open(cabecalho, 'rb'))
        contadorCabecalho = -1
        for i in self.arquivosOrigem:
            for j in range(i.getNumPages()):
                contadorCabecalho += 1
                paginaCabecalho = cabecalho.getPage(contadorCabecalho)
                pagina = i.getPage(j)
                pagina.mergePage(paginaCabecalho)
                self.arquivoDestino.addPage(pagina)
        
        with open(self.nomeArquivoDestino, 'wb') as f:
            self.arquivoDestino.write(f)

    def numeroPaginas(self):
        numeroPaginas = 0
        for i in self.arquivosOrigem:
            numeroPaginas += i.getNumPages()
        return numeroPaginas
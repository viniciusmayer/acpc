from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
import glob, sys

class PDFService(object):

    def __init__(self, pastaOrigem, destino):
        self.arquivosOrigem = [] 
        contador = 0
        for arquivo in glob.iglob(pastaOrigem + '**/a*.pdf', recursive=True):
            try:
                pdfFile = PdfFileReader(open(arquivo, 'rb'))
                if not pdfFile.isEncrypted:
                    self.arquivosOrigem.append(pdfFile)
                    contador += 1
                    print('{0} arquivos lidos: {1}'.format(contador, arquivo))
            except:
                print('ERROR reading: {0}'.format(arquivo))
                print(sys.exc_info())
        self.nomeArquivoDestino = destino
        self.arquivoDestino = PdfFileWriter()

    def numeroPaginas(self):
        numeroPaginas = 0
        for i in self.arquivosOrigem:
            try:
                numeroPaginas += i.getNumPages()
            except:
                #TO DO remover arquivos com erro
                print('ERROR: {0}'.format(i.getDocumentInfo()))
                print(sys.exc_info())
            
        return numeroPaginas

    def gerarCabecalho(self, arquivoDestino, numeroPaginas):
        c = canvas.Canvas(arquivoDestino)
        largura, altura = A4
        for pagina in range(1, numeroPaginas + 1):
            c.drawRightString(largura - cm, altura - cm, '{0}/{1}'.format(pagina, numeroPaginas))
            c.showPage()
            print('pagina gerada: {0}/{1}'.format(pagina, numeroPaginas))
        c.save()

    def gerarArquivo(self, cabecalho, numeroPaginas):
        cabecalho = PdfFileReader(open(cabecalho, 'rb'))
        numeroPagina = -1
        for i in self.arquivosOrigem:
            for j in range(i.getNumPages()):
                numeroPagina += 1
                paginaCabecalho = cabecalho.getPage(numeroPagina)
                pagina = i.getPage(j)
                try:
                    pagina.mergePage(paginaCabecalho)
                    self.arquivoDestino.addPage(pagina)
                    print('pagina processada: {0}/{1}'.format(numeroPagina, numeroPaginas))
                except:
                    #TO DO remover arquivos com erro
                    print('ERROR: {0}'.format(i.getDocumentInfo()))
                    print(sys.exc_info())
        
        with open(self.nomeArquivoDestino, 'wb') as f:
            self.arquivoDestino.write(f)

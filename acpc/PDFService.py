import glob, sys

from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


class PDFService(object):

    def __init__(self, origem):
        self.arquivos = {}
        self.paginas = 0 
        for arquivo in glob.iglob(origem + '**/a*.pdf', recursive=True):
            try:
                pdfFile = PdfFileReader(open(arquivo, 'rb'))
                if not pdfFile.isEncrypted:
                    numeroPaginas = pdfFile.getNumPages()
                    self.paginas += numeroPaginas 
                    self.arquivos[arquivo] = pdfFile
                    print('{0} file add: {1}'.format(len(self.arquivos), arquivo))
                    print('pages: {0}/{1}'.format(numeroPaginas, self.paginas))
            except:
                print('ERROR reading file: {0}'.format(arquivo))
                print(sys.exc_info())

    def gerarCabecalho(self, destino):
        c = canvas.Canvas(destino)
        largura, altura = A4
        for pagina in range(1, self.paginas + 1):
            c.drawRightString(largura - cm, altura - cm, '{0}/{1}'.format(pagina, self.paginas))
            c.showPage()
            print('header page written: {0}/{1}'.format(pagina, self.paginas))
        c.save()

    def gerarArquivo(self, cabecalho, destino):
        cabecalho = PdfFileReader(open(cabecalho, 'rb'))
        arquivoDestino = PdfFileWriter()
        numeroPaginaCabecalho = 0
        for nomeArquivo in self.arquivos.keys():
            arquivo = self.arquivos[nomeArquivo]
            for numeroPagina in range(arquivo.getNumPages()):
                paginaCabecalho = cabecalho.getPage(numeroPaginaCabecalho)
                pagina = arquivo.getPage(numeroPagina)
                try:
                    pagina.mergePage(paginaCabecalho)
                    arquivoDestino.addPage(pagina)
                    numeroPaginaCabecalho += 1
                    print('page written: {0}/{1}'.format(numeroPaginaCabecalho, self.paginas))
                except:
                    print('ERROR writing page {0}: {1}'.format(numeroPagina, nomeArquivo))
                    print(sys.exc_info())
        
        with open(destino, 'wb') as f:
            arquivoDestino.write(f)

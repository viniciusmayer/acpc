import glob, sys
import uuid

from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.lib.colors import Color
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


class PDFService(object):

    def __init__(self, origem):
        self.arquivos = {}
        self.paginas = 0
 
        for arquivo in glob.iglob(origem + '**/*.pdf', recursive=True):
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

    def gerarCabecalho(self, largura, altura, pagina, assinatura, tmp):
        nomeArquivo = '{0}{1}'.format(tmp, str(uuid.uuid4()))
        c = canvas.Canvas(nomeArquivo, pagesize=(largura, altura))
        # fundo da paginacao
        color = Color(255, 255, 255, alpha=0.5)
        c.setFillColor(color)
        c.setStrokeColor(color)
        c.rect(largura - (2.5 * cm), altura - (1.1 * cm), (1.9 * cm), (0.5 * cm), fill=1)
        # paginacao
        c.setFillColor(Color(0, 0, 0, alpha=1))
        c.drawRightString(largura - (0.75 * cm), altura - (1 * cm), '{0}/{1}'.format(pagina, self.paginas))
        # assinatura
        c.drawImage(assinatura, largura - (2 * cm), 0, width=(2 * cm), height=(2 * cm))
        # gerar pagina
        c.showPage()
        c.save()
        cabecalho = PdfFileReader(open(nomeArquivo, 'rb'))
        return cabecalho.getPage(0)

    def gerarArquivo(self, destino, assinatura, tmp, limite=None):
        arquivoDestino = PdfFileWriter()
        numeroPaginaCabecalho = 1
        for nomeArquivo in self.arquivos.keys():
            if limite is not None and numeroPaginaCabecalho > limite:
                break
            arquivo = self.arquivos[nomeArquivo]
            for numeroPagina in range(arquivo.getNumPages()):
                pagina = arquivo.getPage(numeroPagina)
                largura = float(pagina.mediaBox.getWidth())
                altura = float(pagina.mediaBox.getHeight())
                paginaCabecalho = self.gerarCabecalho(largura, altura, numeroPaginaCabecalho, assinatura, tmp)
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

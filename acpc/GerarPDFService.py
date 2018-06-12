import glob, uuid, psycopg2

from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.lib.colors import Color
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


class GerarPDFService(object):

    def __init__(self, origem):
        self.conn = psycopg2.connect("dbname='acpc' user='acpc' host='localhost' password='v1n1c1u5'")
        self.cursor = self.conn.cursor()
        self.arquivos = {}
        self.paginas = 0
        for arquivo in glob.iglob(origem + '**/*.pdf', recursive=True):
            pdfFile = PdfFileReader(open(arquivo, 'rb'))
            if not pdfFile.isEncrypted:
                numeroPaginas = pdfFile.getNumPages()
                self.paginas += numeroPaginas 
                self.arquivos[arquivo] = pdfFile

    def gerarCabecalho(self, largura, altura, pagina, assinatura, tmp):
        arquivo = '{0}{1}'.format(tmp, str(uuid.uuid4()))
        c = canvas.Canvas(arquivo, pagesize=(largura, altura))
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
        cabecalho = PdfFileReader(open(arquivo, 'rb'))
        return cabecalho.getPage(0)

    def processar(self, nomeArquivoDestino, assinatura, tmp, limite=None):
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
                pagina.mergePage(paginaCabecalho)
                arquivoDestino.addPage(pagina)
                numeroPaginaCabecalho += 1
        with open(nomeArquivoDestino, 'wb') as f:
            arquivoDestino.write(f)

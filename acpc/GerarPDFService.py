import glob, uuid, os

from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.lib.colors import Color
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


class GerarPDFService(object):

    def __init__(self, origem, tmp):
        if not os.path.exists(tmp):
            os.makedirs(tmp)
        self.arquivos = {}
        self.paginas = 0
        for arquivo in glob.iglob(origem + '**/*.pdf', recursive=True):
            pdfFile = PdfFileReader(open(arquivo, 'rb'))
            if not pdfFile.isEncrypted:
                self.paginas += pdfFile.getNumPages() 
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

    def processar(self, arquivoDestino, assinatura, tmp, limite=None):
        _arquivoDestino = PdfFileWriter()
        numeroPaginaCabecalho = 1
        for nomeArquivo in self.arquivos.keys():
            if limite is not None and numeroPaginaCabecalho > limite:
                break
            arquivo = self.arquivos[nomeArquivo]
            for numeroPagina in range(0, arquivo.getNumPages()):
                pagina = arquivo.getPage(numeroPagina)
                largura = float(pagina.mediaBox.getWidth())
                altura = float(pagina.mediaBox.getHeight())
                paginaCabecalho = self.gerarCabecalho(largura, altura, numeroPaginaCabecalho, assinatura, tmp)
                pagina.mergePage(paginaCabecalho)
                _arquivoDestino.addPage(pagina)
                print('pagina gerada: {0}/{1}'.format(numeroPaginaCabecalho, self.paginas))
                numeroPaginaCabecalho += 1
        with open(arquivoDestino, 'wb') as f:
            _arquivoDestino.write(f)

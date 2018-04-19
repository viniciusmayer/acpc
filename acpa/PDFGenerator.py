from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

class PDFGenerator(object):
    def processar(self, arquivoDestino, numeroPaginas):
        c = canvas.Canvas(arquivoDestino)
        largura, altura = A4
        for pagina in range(1, numeroPaginas + 1):
            c.drawRightString(largura - cm, altura - cm, '{0}/{1}'.format(pagina, numeroPaginas))
            c.showPage()
        c.save()

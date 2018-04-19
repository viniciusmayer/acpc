from reportlab.pdfgen import canvas

class PDFGenerator(object):
    def __init__(self, point = 1, inch = 72):
        self.point = point
        self.inch = inch

    def processar(self, nomeArquivoDestino, numeroPaginas):
        c = canvas.Canvas(nomeArquivoDestino)
        c.setStrokeColorRGB(0, 0, 0)
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica", 12 * self.point)
        
        for pagina in range(1, numeroPaginas + 1):
            for texto in ('{0}/{1}'.format(pagina, numeroPaginas)).split('\n'):
                c.drawRightString(self.inch, self.inch, texto)
            c.showPage()
        c.save()

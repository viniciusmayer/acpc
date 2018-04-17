from acpa.PDFService import PDFService
if __name__ == '__main__':
    processar = PDFService('../files/cabecalho.pdf'
                           , '../files/pdfs/'
                           , '../files/destino.pdf')
    processar.processar()
    
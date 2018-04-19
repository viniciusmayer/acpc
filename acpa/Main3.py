from acpa.PDFGenerator import PDFGenerator

if __name__ == '__main__':
    processar = PDFGenerator()
    processar.processar('destino.pdf', 3)
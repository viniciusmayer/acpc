from acpa.PDFService import PDFService
from acpa.PDFGenerator import PDFGenerator

if __name__ == '__main__':
    arquivoCabecalho = '../files/cabecalho.pdf'
    pastaPDFs = '../files/pdfs/'
    arquivoFinal = '../files/destino.pdf'
    
    pdfs = PDFService(pastaPDFs, arquivoFinal)
    cabecalho = PDFGenerator()
    cabecalho.processar(arquivoCabecalho, pdfs.numeroPaginas())
    pdfs.processar(arquivoCabecalho)

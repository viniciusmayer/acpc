from acpa.PDFService import PDFService

if __name__ == '__main__':
    arquivoCabecalho = '../files/cabecalho.pdf'
    pastaPDFs = '/Users/eleonor.mayer/Documents/'
    arquivoFinal = '../files/destino.pdf'
    
    print('===> reading files')
    service = PDFService(pastaPDFs)
    print('===> writing header')
    service.gerarCabecalho(arquivoCabecalho)
    print('===> writing file')
    service.gerarArquivo(arquivoCabecalho, arquivoFinal)

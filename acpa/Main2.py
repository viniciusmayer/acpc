from acpa.PDFService import PDFService

if __name__ == '__main__':
    arquivoCabecalho = '../files/cabecalho.pdf'
    pastaPDFs = '/home/eleonorvinicius/Documents/'
    arquivoFinal = '../files/destino.pdf'
    
    print('===> lendo arquivos')
    service = PDFService(pastaPDFs, arquivoFinal)
    print('===> gerando cabecalho')
    numeroPaginas = service.numeroPaginas()
    service.gerarCabecalho(arquivoCabecalho, numeroPaginas)
    print('===> gerando arquivo')
    service.gerarArquivo(arquivoCabecalho, numeroPaginas)

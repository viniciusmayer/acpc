from acpa.PDFService import PDFService

if __name__ == '__main__':
    cabecalho = '../files/cabecalho.pdf'
    pastaPDFs = '/home/eleonorvinicius/Documents/'
    destino = '../files/destino.pdf'
    
    print('===> reading files')
    service = PDFService(pastaPDFs)
    print('===> writing header')
    service.gerarCabecalho(cabecalho)
    print('===> writing file')
    service.gerarArquivo(cabecalho, destino)
    print('===> file written')
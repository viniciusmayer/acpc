from acpc.PDFService import PDFService
import time

def getElapsedTime(start):
    end = time.time()
    m, s = divmod(end - start, 60)
    h, m = divmod(m, 60)
    return '{0}:{1}:{2}'.format(h, m, s)

if __name__ == '__main__':
    print('===> begin')
    inicioA = time.time()
    cabecalho = '../files/cabecalho.pdf'
    pastaPDFs = '../files/pdfs/'
    destino = '../files/destino.pdf'
    
    print('===> reading files')
    inicio = time.time()
    service = PDFService(pastaPDFs)
    print('===> files read: {0}'.format(getElapsedTime(inicio)))
    
    print('===> writing header')
    inicio = time.time()
    service.gerarCabecalho(cabecalho)
    print('===> header written: {0}'.format(getElapsedTime(inicio)))
    
    print('===> writing file')
    inicio = time.time()
    service.gerarArquivo(cabecalho, destino)
    print('===> file written: {0}'.format(getElapsedTime(inicio)))
    
    fim = time.time()
    print('===> end: {0}'.format(getElapsedTime(inicioA)))
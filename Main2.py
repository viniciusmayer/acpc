import shutil, sys, os

from acpc.PDFService import PDFService


if __name__ == '__main__':
    print('===> begin')
    pastaPDFs = 'files/pdfs/'
    destino = 'files/destino.pdf'
    tmp = 'files/tmp/'
    
    print('===> reading files')
    service = PDFService(pastaPDFs)
    
    print('===> writing file')
    limite = int(sys.argv[1]) if len(sys.argv) > 1 else None
    
    if not os.path.exists(tmp):
        os.makedirs(tmp)
    service.gerarArquivo(destino, 'files/assinatura.jpg', tmp, limite)
    
    print('===> system cleaning')
    shutil.rmtree(tmp)
    print('===> end')
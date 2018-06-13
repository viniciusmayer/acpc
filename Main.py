import os
import shutil
import sys

from acpc.GerarPDFService import GerarPDFService
from acpc.ImportarLattesService import ImportarLattesService
from acpc.ImportarPDFsService import ImportarPDFsService


def importarLattes(lattes):
    print()
    print('inicio - importar lattes')
    processar = ImportarLattesService(lattes)
    processar.processar('TRABALHO-EM-EVENTOS', 'DADOS-BASICOS-DO-TRABALHO', 'TITULO-DO-TRABALHO', 'ANO-DO-TRABALHO')
    processar.processar('ARTIGO-PUBLICADO', 'DADOS-BASICOS-DO-ARTIGO', 'TITULO-DO-ARTIGO', 'ANO-DO-ARTIGO')
    processar.processar('LIVRO-PUBLICADO-OU-ORGANIZADO', 'DADOS-BASICOS-DO-LIVRO', 'TITULO-DO-LIVRO')
    processar.processar('CAPITULO-DE-LIVRO-PUBLICADO', 'DADOS-BASICOS-DO-CAPITULO', 'TITULO-DO-CAPITULO-DO-LIVRO')
    processar.processar('TRABALHO-TECNICO', 'DADOS-BASICOS-DO-TRABALHO-TECNICO', 'TITULO-DO-TRABALHO-TECNICO')
    processar.processar('APRESENTACAO-DE-TRABALHO', 'DADOS-BASICOS-DA-APRESENTACAO-DE-TRABALHO')
    processar.processar('CURSO-DE-CURTA-DURACAO-MINISTRADO', 'DADOS-BASICOS-DE-CURSOS-CURTA-DURACAO-MINISTRADO')
    processar.processar('ORGANIZACAO-DE-EVENTO', 'DADOS-BASICOS-DA-ORGANIZACAO-DE-EVENTO')
    processar.processar('OUTRAS-BANCAS-JULGADORAS', 'DADOS-BASICOS-DE-OUTRAS-BANCAS-JULGADORAS')
    processar.processar('PARTICIPACAO-EM-CONGRESSO', 'DADOS-BASICOS-DA-PARTICIPACAO-EM-CONGRESSO', 'TITULO', 'ANO', 'NATUREZA', 'DETALHAMENTO-DA-PARTICIPACAO-EM-CONGRESSO')
    processar.processar('PARTICIPACAO-EM-SEMINARIO', 'DADOS-BASICOS-DA-PARTICIPACAO-EM-SEMINARIO', 'TITULO', 'ANO', 'NATUREZA', 'DETALHAMENTO-DA-PARTICIPACAO-EM-SEMINARIO')
    processar.processar('PARTICIPACAO-EM-SIMPOSIO', 'DADOS-BASICOS-DA-PARTICIPACAO-EM-SIMPOSIO', 'TITULO', 'ANO', 'NATUREZA', 'DETALHAMENTO-DA-PARTICIPACAO-EM-SIMPOSIO')
    processar.processar('PARTICIPACAO-EM-ENCONTRO', 'DADOS-BASICOS-DA-PARTICIPACAO-EM-ENCONTRO', 'TITULO', 'ANO', 'NATUREZA', 'DETALHAMENTO-DA-PARTICIPACAO-EM-ENCONTRO')
    processar.processar('OUTRAS-PARTICIPACOES-EM-EVENTOS-CONGRESSOS', 'DADOS-BASICOS-DE-OUTRAS-PARTICIPACOES-EM-EVENTOS-CONGRESSOS', 'TITULO', 'ANO', 'NATUREZA', 'DETALHAMENTO-DE-OUTRAS-PARTICIPACOES-EM-EVENTOS-CONGRESSOS')
    print('fim - importar lattes')
    
def importarPDFs(origem, destino):
    print()
    print('inicio - importar pdfs')
    service = ImportarPDFsService(destino)
    service.processar(origem, destino)
    print('fim - importar lattes')

def gerarPDF(origem, assinatura, tmp, limite):
    print()
    print('inicio - gerar pdf')
    service = GerarPDFService(origem, tmp)
    service.processar(assinatura, tmp)
    print('fim - gerar pdf')

lattes = 'files/lattes/curriculo.xml'
origem = 'files/pdfs/'
destino = 'files/uploads/'
assinatura = 'files/assinatura.jpg'
tmp = 'files/tmp/'
if __name__ == '__main__':
    print()
    print('inicio')
    for i in range(1, len(sys.argv)):
        comando = sys.argv[i]
        if (comando == 'importarlattes'):
            importarLattes(lattes)
        elif (comando == 'importarpdfs'):
            importarPDFs(origem, destino)
        elif (comando == 'gerarpdf'):
            limite = int(sys.argv[sys.argv.index('-l') + 1]) if '-l' in sys.argv else None
            gerarPDF(destino, assinatura, tmp, limite)
        elif (comando == '-l'):
            break
        else:
            print('= help =')
            print('command: main [options,]')
            print('options:')
            print('        importarlattes')
            print('        importarpdfs')
            print('        gerarpdf [-l <number of pages to be generated>]')
            print('example: main importarlattes importarpfds')
            print('example: main importarpfds gerarpdf -l 35')
    if os.path.exists(tmp):
        shutil.rmtree(tmp)
    print('fim')

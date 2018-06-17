import os
import shutil
import sys

from acpc.GerarPDFService import GerarPDFService
from acpc.ImportarLattesService import ImportarLattesService
from acpc.ImportarPDFsService import ImportarPDFsService


def importarLattes(lattes):
    print()
    print('inicio - importar lattes')
    service = ImportarLattesService(lattes)
    service.processar(tagName='GRADUACAO', tituloAttributeName='TITULO-DO-TRABALHO-DE-CONCLUSAO-DE-CURSO', anoAttributeName='ANO-DE-INICIO', anoFimAttributeName='ANO-DE-CONCLUSAO')
    service.processar(tagName='MESTRADO', tituloAttributeName='TITULO-DA-DISSERTACAO-TESE', anoAttributeName='ANO-DE-INICIO', anoFimAttributeName='ANO-DE-CONCLUSAO')
    service.processar(tagName='DOUTORADO', tituloAttributeName='TITULO-DA-DISSERTACAO-TESE', anoAttributeName='ANO-DE-INICIO', anoFimAttributeName='ANO-DE-CONCLUSAO')
    service.processar(tagName='FORMACAO-COMPLEMENTAR-DE-EXTENSAO-UNIVERSITARIA', tituloAttributeName='NOME-CURSO', anoAttributeName='ANO-DE-INICIO', anoFimAttributeName='ANO-DE-CONCLUSAO')
    service.processar(tagName='FORMACAO-COMPLEMENTAR-CURSO-DE-CURTA-DURACAO', tituloAttributeName='NOME-CURSO', anoAttributeName='ANO-DE-INICIO', anoFimAttributeName='ANO-DE-CONCLUSAO')
    
    service.processar(tagName='ATUACAO-PROFISSIONAL'
                      , dadosBasicosTagName=None
                      , tituloAttributeName='NOME-INSTITUICAO'
                      , anoAttributeName='ANO-INICIO'
                      , anoFimAttributeName='ANO-FIM'
                      , naturezaAttributeName='OUTRO-VINCULO-INFORMADO'
                      , detalhamentoTagName='VINCULOS'
                      , nomeDoEventoAttributeName='OUTRO-ENQUADRAMENTO-FUNCIONAL-INFORMADO')
    
    service.processar(tagName='PROJETO-DE-PESQUISA', tituloAttributeName='NOME-DO-PROJETO', anoAttributeName='ANO-INICIO', anoFimAttributeName='ANO-FIM')
    service.processar(tagName='PREMIO-TITULO', tituloAttributeName='NOME-DO-PREMIO-OU-TITULO', anoAttributeName='ANO-DA-PREMIACAO')
    service.processar(tagName='ARTIGO-PUBLICADO', dadosBasicosTagName='DADOS-BASICOS-DO-ARTIGO', tituloAttributeName='TITULO-DO-ARTIGO', anoAttributeName='ANO-DO-ARTIGO')
    service.processar(tagName='LIVRO-PUBLICADO-OU-ORGANIZADO', dadosBasicosTagName='DADOS-BASICOS-DO-LIVRO', tituloAttributeName='TITULO-DO-LIVRO', anoAttributeName='ANO')
    service.processar(tagName='CAPITULO-DE-LIVRO-PUBLICADO', dadosBasicosTagName='DADOS-BASICOS-DO-CAPITULO', tituloAttributeName='TITULO-DO-CAPITULO-DO-LIVRO')
    service.processar(tagName='TRABALHO-EM-EVENTOS', dadosBasicosTagName='DADOS-BASICOS-DO-TRABALHO', tituloAttributeName='TITULO-DO-TRABALHO', anoAttributeName='ANO-DO-TRABALHO', anoFimAttributeName='ANO-DO-TRABALHO')
    service.processar(tagName='APRESENTACAO-DE-TRABALHO', dadosBasicosTagName='DADOS-BASICOS-DA-APRESENTACAO-DE-TRABALHO')
    service.processar(tagName='TRABALHO-TECNICO', dadosBasicosTagName='DADOS-BASICOS-DO-TRABALHO-TECNICO', tituloAttributeName='TITULO-DO-TRABALHO-TECNICO')
    service.processar(tagName='CURSO-DE-CURTA-DURACAO-MINISTRADO', dadosBasicosTagName='DADOS-BASICOS-DE-CURSOS-CURTA-DURACAO-MINISTRADO')
    service.processar(tagName='OUTRAS-BANCAS-JULGADORAS', dadosBasicosTagName='DADOS-BASICOS-DE-OUTRAS-BANCAS-JULGADORAS')
    service.processar(tagName='PARTICIPACAO-EM-SEMINARIO', dadosBasicosTagName='DADOS-BASICOS-DA-PARTICIPACAO-EM-SEMINARIO', detalhamentoTagName='DETALHAMENTO-DA-PARTICIPACAO-EM-SEMINARIO')
    service.processar(tagName='PARTICIPACAO-EM-CONGRESSO', dadosBasicosTagName='DADOS-BASICOS-DA-PARTICIPACAO-EM-CONGRESSO', detalhamentoTagName='DETALHAMENTO-DA-PARTICIPACAO-EM-CONGRESSO')
    service.processar(tagName='PARTICIPACAO-EM-SIMPOSIO', dadosBasicosTagName='DADOS-BASICOS-DA-PARTICIPACAO-EM-SIMPOSIO', detalhamentoTagName='DETALHAMENTO-DA-PARTICIPACAO-EM-SIMPOSIO')
    service.processar(tagName='PARTICIPACAO-EM-ENCONTRO', dadosBasicosTagName='DADOS-BASICOS-DA-PARTICIPACAO-EM-ENCONTRO', detalhamentoTagName='DETALHAMENTO-DA-PARTICIPACAO-EM-ENCONTRO')
    service.processar(tagName='ORGANIZACAO-DE-EVENTO', dadosBasicosTagName='DADOS-BASICOS-DA-ORGANIZACAO-DE-EVENTO')
    service.processar(tagName='OUTRAS-PARTICIPACOES-EM-EVENTOS-CONGRESSOS', dadosBasicosTagName='DADOS-BASICOS-DE-OUTRAS-PARTICIPACOES-EM-EVENTOS-CONGRESSOS', detalhamentoTagName='DETALHAMENTO-DE-OUTRAS-PARTICIPACOES-EM-EVENTOS-CONGRESSOS')
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

from datetime import datetime
import os
import shutil
import sys
import uuid

from acpc.GerarEventoService import GerarEventoService
from acpc.GerarPDFService import GerarPDFService
from acpc.ImportarLattesService import ImportarLattesService
from acpc.ImportarPDFsService import ImportarPDFsService


def importarLattes(lattes):
    print()
    print('inicio - importar lattes')
    service = ImportarLattesService(lattes)
    service.processar(tagOrdem=0, tagName='GRADUACAO', tituloAttributeName='TITULO-DO-TRABALHO-DE-CONCLUSAO-DE-CURSO', anoAttributeName='ANO-DE-INICIO', anoFimAttributeName='ANO-DE-CONCLUSAO')
    service.processar(tagOrdem=1, tagName='MESTRADO', tituloAttributeName='TITULO-DA-DISSERTACAO-TESE', anoAttributeName='ANO-DE-INICIO', anoFimAttributeName='ANO-DE-CONCLUSAO')
    service.processar(tagOrdem=2, tagName='DOUTORADO', tituloAttributeName='TITULO-DA-DISSERTACAO-TESE', anoAttributeName='ANO-DE-INICIO', anoFimAttributeName='ANO-DE-CONCLUSAO')
    service.processar(tagOrdem=3, tagName='FORMACAO-COMPLEMENTAR-DE-EXTENSAO-UNIVERSITARIA', tituloAttributeName='NOME-CURSO', anoAttributeName='ANO-DE-INICIO', anoFimAttributeName='ANO-DE-CONCLUSAO')
    service.processar(tagOrdem=4, tagName='FORMACAO-COMPLEMENTAR-CURSO-DE-CURTA-DURACAO', tituloAttributeName='NOME-CURSO', anoAttributeName='ANO-DE-INICIO', anoFimAttributeName='ANO-DE-CONCLUSAO')
    service.processar(tagOrdem=5, tagName='ATUACAO-PROFISSIONAL', tituloAttributeName='NOME-INSTITUICAO', anoAttributeName='ANO-INICIO', anoFimAttributeName='ANO-FIM'
                      , naturezaAttributeName='OUTRO-VINCULO-INFORMADO', detalhamentoTagName='VINCULOS', nomeDoEventoAttributeName='OUTRO-ENQUADRAMENTO-FUNCIONAL-INFORMADO')
    service.processar(tagOrdem=6, tagName='PROJETO-DE-PESQUISA', tituloAttributeName='NOME-DO-PROJETO', anoAttributeName='ANO-INICIO', anoFimAttributeName='ANO-FIM')
    service.processar(tagOrdem=7, tagName='PREMIO-TITULO', tituloAttributeName='NOME-DO-PREMIO-OU-TITULO', anoAttributeName='ANO-DA-PREMIACAO')
    service.processar(tagOrdem=8, tagName='ARTIGO-PUBLICADO', dadosBasicosTagName='DADOS-BASICOS-DO-ARTIGO', tituloAttributeName='TITULO-DO-ARTIGO', anoAttributeName='ANO-DO-ARTIGO')
    service.processar(tagOrdem=9, tagName='LIVRO-PUBLICADO-OU-ORGANIZADO', dadosBasicosTagName='DADOS-BASICOS-DO-LIVRO', tituloAttributeName='TITULO-DO-LIVRO', anoAttributeName='ANO')
    service.processar(tagOrdem=10, tagName='CAPITULO-DE-LIVRO-PUBLICADO', dadosBasicosTagName='DADOS-BASICOS-DO-CAPITULO', tituloAttributeName='TITULO-DO-CAPITULO-DO-LIVRO')
    service.processar(tagOrdem=11, tagName='TRABALHO-EM-EVENTOS', dadosBasicosTagName='DADOS-BASICOS-DO-TRABALHO', tituloAttributeName='TITULO-DO-TRABALHO', anoAttributeName='ANO-DO-TRABALHO'
                      , anoFimAttributeName='ANO-DO-TRABALHO')
    service.processar(tagOrdem=12, tagName='APRESENTACAO-DE-TRABALHO', dadosBasicosTagName='DADOS-BASICOS-DA-APRESENTACAO-DE-TRABALHO')
    service.processar(tagOrdem=13, tagName='TRABALHO-TECNICO', dadosBasicosTagName='DADOS-BASICOS-DO-TRABALHO-TECNICO', tituloAttributeName='TITULO-DO-TRABALHO-TECNICO')
    service.processar(tagOrdem=14, tagName='CURSO-DE-CURTA-DURACAO-MINISTRADO', dadosBasicosTagName='DADOS-BASICOS-DE-CURSOS-CURTA-DURACAO-MINISTRADO')
    service.processar(tagOrdem=15, tagName='OUTRAS-BANCAS-JULGADORAS', dadosBasicosTagName='DADOS-BASICOS-DE-OUTRAS-BANCAS-JULGADORAS')
    service.processar(tagOrdem=16, tagName='PARTICIPACAO-EM-SEMINARIO', dadosBasicosTagName='DADOS-BASICOS-DA-PARTICIPACAO-EM-SEMINARIO', detalhamentoTagName='DETALHAMENTO-DA-PARTICIPACAO-EM-SEMINARIO')
    service.processar(tagOrdem=17, tagName='PARTICIPACAO-EM-CONGRESSO', dadosBasicosTagName='DADOS-BASICOS-DA-PARTICIPACAO-EM-CONGRESSO', detalhamentoTagName='DETALHAMENTO-DA-PARTICIPACAO-EM-CONGRESSO')
    service.processar(tagOrdem=18, tagName='PARTICIPACAO-EM-SIMPOSIO', dadosBasicosTagName='DADOS-BASICOS-DA-PARTICIPACAO-EM-SIMPOSIO', detalhamentoTagName='DETALHAMENTO-DA-PARTICIPACAO-EM-SIMPOSIO')
    service.processar(tagOrdem=19, tagName='PARTICIPACAO-EM-ENCONTRO', dadosBasicosTagName='DADOS-BASICOS-DA-PARTICIPACAO-EM-ENCONTRO', detalhamentoTagName='DETALHAMENTO-DA-PARTICIPACAO-EM-ENCONTRO')
    service.processar(tagOrdem=20, tagName='ORGANIZACAO-DE-EVENTO', dadosBasicosTagName='DADOS-BASICOS-DA-ORGANIZACAO-DE-EVENTO')
    service.processar(tagOrdem=21, tagName='OUTRAS-PARTICIPACOES-EM-EVENTOS-CONGRESSOS', dadosBasicosTagName='DADOS-BASICOS-DE-OUTRAS-PARTICIPACOES-EM-EVENTOS-CONGRESSOS'
                      , detalhamentoTagName='DETALHAMENTO-DE-OUTRAS-PARTICIPACOES-EM-EVENTOS-CONGRESSOS')
    print('fim - importar lattes')
    
def importarPDFs(origem, destino):
    print()
    print('inicio - importar pdfs')
    service = ImportarPDFsService(destino)
    service.processar(origem, destino)
    print('fim - importar lattes')

def gerarPDF(origem, assinatura, tmp):
    print()
    print('inicio - gerar pdf')
    service = GerarPDFService(origem, tmp)
    service.processar(assinatura, tmp)
    print('fim - gerar pdf')

def gerarEvento(nome, quando):
    print()
    print('inicio - gerar evento')
    service = GerarEventoService()
    service.processar(nome, quando)
    print('fim - gerar evento')

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
            #limite = int(sys.argv[sys.argv.index('-l') + 1]) if '-l' in sys.argv else None
            gerarPDF(destino, assinatura, tmp)
        elif (comando == 'gerarevento'):
            gerarEvento(str(uuid.uuid4()), datetime.today())
        else:
            print('= help =')
            print('command: main [options,]')
            print('options:')
            print('        importarlattes')
            print('        importarpdfs')
            print('        gerarevento')
            print('        gerarpdf')
            print('example: main importarlattes importarpfds gerarevento gerarpdf')
            print('example: main importarpfds gerarpdf')
    if os.path.exists(tmp):
        shutil.rmtree(tmp)
    print('fim')

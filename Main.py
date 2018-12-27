from datetime import datetime
import os
import shutil
import sys
import uuid

from acpc.FazerBackupService import FazerBackupService
from acpc.GerarEventoService import GerarEventoService
from acpc.GerarPDFService import GerarPDFService
from acpc.ImportarLattesService import ImportarLattesService
from acpc.ImportarPDFsService import ImportarPDFsService


def importarLattes(lattes, armazenamento):
    print()
    print('inicio - importar lattes', armazenamento)
    service = ImportarLattesService(lattes, armazenamento)
    service.processar(tagOrdem=0, tagName='GRADUACAO'
                      , tituloAttributeName='TITULO-DO-TRABALHO-DE-CONCLUSAO-DE-CURSO'
                      , anoAttributeName='ANO-DE-INICIO'
                      , anoFimAttributeName='ANO-DE-CONCLUSAO')
    service.processar(tagOrdem=1, tagName='MESTRADO'
                      , tituloAttributeName='TITULO-DA-DISSERTACAO-TESE'
                      , anoAttributeName='ANO-DE-INICIO'
                      , anoFimAttributeName='ANO-DE-CONCLUSAO')
    service.processar(tagOrdem=2, tagName='DOUTORADO'
                      , tituloAttributeName='TITULO-DA-DISSERTACAO-TESE'
                      , anoAttributeName='ANO-DE-INICIO'
                      , anoFimAttributeName='ANO-DE-CONCLUSAO')
    service.processar(tagOrdem=3, tagName='FORMACAO-COMPLEMENTAR-DE-EXTENSAO-UNIVERSITARIA'
                      , tituloAttributeName='NOME-CURSO'
                      , anoAttributeName='ANO-DE-INICIO'
                      , anoFimAttributeName='ANO-DE-CONCLUSAO')
    service.processar(tagOrdem=4, tagName='FORMACAO-COMPLEMENTAR-CURSO-DE-CURTA-DURACAO'
                      , tituloAttributeName='NOME-CURSO'
                      , anoAttributeName='ANO-DE-INICIO'
                      , anoFimAttributeName='ANO-DE-CONCLUSAO')
    service.processar(tagOrdem=7, tagName='PREMIO-TITULO'
                      , tituloAttributeName='NOME-DO-PREMIO-OU-TITULO'
                      , anoAttributeName='ANO-DA-PREMIACAO'
                      , entidadeTagName='NOME-DA-ENTIDADE-PROMOTORA')
    #inicio detalhamentoTagName
    service.processar(tagOrdem=5, tagName='ATUACAO-PROFISSIONAL'
                      , tituloAttributeName=None #FIXME informar nome do evento?
                      , anoAttributeName='ANO-INICIO'
                      , anoFimAttributeName='ANO-FIM'
                      , naturezaAttributeName='OUTRO-VINCULO-INFORMADO'
                      , detalhamentoTagName='VINCULOS'
                      , nomeDoEventoAttributeName='OUTRO-ENQUADRAMENTO-FUNCIONAL-INFORMADO')
    #inicio dadosBasicosTagName
    service.processar(tagOrdem=6, tagName='PARTICIPACAO-EM-PROJETO'
                      , tituloAttributeName='NOME-DO-PROJETO'
                      , dadosBasicosTagName='PROJETO-DE-PESQUISA'
                      , anoAttributeName='ANO-INICIO'
                      , anoFimAttributeName='ANO-FIM'
                      , entidadeTagName='NOME-ORGAO')
    #inicio 3
    service.processar(tagOrdem=8, tagName='ARTIGO-PUBLICADO'
                      , dadosBasicosTagName='DADOS-BASICOS-DO-ARTIGO'
                      , tituloAttributeName='TITULO-DO-ARTIGO'
                      , anoAttributeName='ANO-DO-ARTIGO'
                      , detalhamentoTagName='DETALHAMENTO-DO-ARTIGO'
                      , entidadeTagName='TITULO-DO-PERIODICO-OU-REVISTA')
    service.processar(tagOrdem=9, tagName='LIVRO-PUBLICADO-OU-ORGANIZADO'
                      , dadosBasicosTagName='DADOS-BASICOS-DO-LIVRO'
                      , tituloAttributeName='TITULO-DO-LIVRO'
                      , anoAttributeName='ANO'
                      , detalhamentoTagName='DETALHAMENTO-DO-LIVRO'
                      , entidadeTagName='NOME-DA-EDITORA')
    service.processar(tagOrdem=10, tagName='CAPITULO-DE-LIVRO-PUBLICADO'
                      , dadosBasicosTagName='DADOS-BASICOS-DO-CAPITULO'
                      , tituloAttributeName='TITULO-DO-CAPITULO-DO-LIVRO'
                      , detalhamentoTagName='DETALHAMENTO-DO-CAPITULO'
                      , entidadeTagName='NOME-DA-EDITORA')
    service.processar(tagOrdem=11, tagName='TRABALHO-EM-EVENTOS'
                      , dadosBasicosTagName='DADOS-BASICOS-DO-TRABALHO'
                      , tituloAttributeName='TITULO-DO-TRABALHO'
                      , anoAttributeName='ANO-DO-TRABALHO'
                      , anoFimAttributeName='ANO-DO-TRABALHO'
                      , detalhamentoTagName='DETALHAMENTO-DO-TRABALHO'
                      , nomeDoEventoAttributeName=None
                      , entidadeTagName='NOME-DO-EVENTO')
    service.processar(tagOrdem=12, tagName='APRESENTACAO-DE-TRABALHO'
                      , dadosBasicosTagName='DADOS-BASICOS-DA-APRESENTACAO-DE-TRABALHO'
                      , entidadeTagName='INSTITUICAO-PROMOTORA'
                      , detalhamentoTagName='DETALHAMENTO-DA-APRESENTACAO-DE-TRABALHO'
                      , nomeDoEventoAttributeName=None)
    service.processar(tagOrdem=13, tagName='TRABALHO-TECNICO'
                      , dadosBasicosTagName='DADOS-BASICOS-DO-TRABALHO-TECNICO'
                      , tituloAttributeName='TITULO-DO-TRABALHO-TECNICO')
    service.processar(tagOrdem=14, tagName='CURSO-DE-CURTA-DURACAO-MINISTRADO'
                      , dadosBasicosTagName='DADOS-BASICOS-DE-CURSOS-CURTA-DURACAO-MINISTRADO'
                      , entidadeTagName='INSTITUICAO-PROMOTORA-DO-CURSO'
                      , detalhamentoTagName='DETALHAMENTO-DE-CURSOS-CURTA-DURACAO-MINISTRADO')
    service.processar(tagOrdem=15, tagName='OUTRAS-BANCAS-JULGADORAS'
                      , dadosBasicosTagName='DADOS-BASICOS-DE-OUTRAS-BANCAS-JULGADORAS'
                      , detalhamentoTagName='DETALHAMENTO-DE-OUTRAS-BANCAS-JULGADORAS')
    service.processar(tagOrdem=16, tagName='PARTICIPACAO-EM-SEMINARIO'
                      , dadosBasicosTagName='DADOS-BASICOS-DA-PARTICIPACAO-EM-SEMINARIO'
                      , detalhamentoTagName='DETALHAMENTO-DA-PARTICIPACAO-EM-SEMINARIO')
    service.processar(tagOrdem=17, tagName='PARTICIPACAO-EM-CONGRESSO'
                      , dadosBasicosTagName='DADOS-BASICOS-DA-PARTICIPACAO-EM-CONGRESSO'
                      , detalhamentoTagName='DETALHAMENTO-DA-PARTICIPACAO-EM-CONGRESSO')
    service.processar(tagOrdem=18, tagName='PARTICIPACAO-EM-SIMPOSIO'
                      , dadosBasicosTagName='DADOS-BASICOS-DA-PARTICIPACAO-EM-SIMPOSIO'
                      , detalhamentoTagName='DETALHAMENTO-DA-PARTICIPACAO-EM-SIMPOSIO')
    service.processar(tagOrdem=19, tagName='PARTICIPACAO-EM-ENCONTRO'
                      , dadosBasicosTagName='DADOS-BASICOS-DA-PARTICIPACAO-EM-ENCONTRO'
                      , detalhamentoTagName='DETALHAMENTO-DA-PARTICIPACAO-EM-ENCONTRO')
    service.processar(tagOrdem=20, tagName='ORGANIZACAO-DE-EVENTO'
                      , dadosBasicosTagName='DADOS-BASICOS-DA-ORGANIZACAO-DE-EVENTO'
                      , detalhamentoTagName='DETALHAMENTO-DA-ORGANIZACAO-DE-EVENTO'
                      , entidadeTagName='INSTITUICAO-PROMOTORA')
    service.processar(tagOrdem=21, tagName='OUTRAS-PARTICIPACOES-EM-EVENTOS-CONGRESSOS'
                      , dadosBasicosTagName='DADOS-BASICOS-DE-OUTRAS-PARTICIPACOES-EM-EVENTOS-CONGRESSOS'
                      , detalhamentoTagName='DETALHAMENTO-DE-OUTRAS-PARTICIPACOES-EM-EVENTOS-CONGRESSOS')
    print('fim - importar lattes')
    
def importarPDFs(origem, destino):
    print()
    print('inicio - importar pdfs')
    service = ImportarPDFsService(destino)
    service.processar(origem, destino)
    print('fim - importar pdfs')

def gerarPDF(origem, assinatura, tmp, nomeEvento):
    print()
    print('inicio - gerar pdf')
    service = GerarPDFService(origem, tmp)
    service.processar(assinatura, tmp, nomeEvento)
    print('fim - gerar pdf')

def gerarEvento(nome, quando):
    print()
    print('inicio - gerar evento')
    service = GerarEventoService()
    service.processar(nome, quando)
    print('fim - gerar evento')

def fazerBackup(pgpass, maquina, porta, banco, usuario, quando, destino):
    print()
    print('inicio - fazer backup')
    service = FazerBackupService(pgpass, maquina, porta, banco, usuario, quando, destino)
    service.processar()
    print('fim - fazer backup')

def ajuda():
    print('= HELP =')
    print('Command: python3 Main.py [option]')
    print('Options:')
    print('\t importarlattes[=bancodedados - para escrever a saida em banco de dados. Valor padrao: arquivo]')
    print('\t importarpdfs')
    print('\t gerarevento[=<nome do evento>] - para especificar o event')
    print('\t gerarpdf')
    print('\t fazerbackup')
    print('\t ajuda')
    print('Example: python3 Main.py importarlattes importarpfds gerarevento gerarpdf')
    print('Example: python3 Main.py importarpfds gerarpdf')


lattes = 'files/lattes/curriculo.xml'
origem = 'files/pdfs/'
destino = 'files/uploads/'
assinatura = 'files/assinatura.jpg'
tmp = 'files/tmp/'
pgpass = '/home/eleonorvinicius/.pgpass'
backup = '/home/eleonorvinicius/Dropbox/Backup/'
if __name__ == '__main__':
    j = len(sys.argv)
    if (j > 1):
        print()
        print('inicio')
        executarImportarLattes = False
        executarGerarPDF = False
        executarImportarPDFs = False
        executarGerarEvento = False
        executarFazerBackup = False
        armazenamento = 'FILE'
        nomeEvento = None
        comandoChave, comandoValor = None, None
        for i in range(1, len(sys.argv)):
            if (sys.argv[i].find('=') > 1): comandoChave, comandoValor = sys.argv[i].split('=')
            else: comandoChave = sys.argv[i]
            if (comandoChave == 'importarlattes'):
                executarImportarLattes = True
                if (comandoValor == 'bancodedados'): armazenamento = 'DATABASE'
            elif (comandoChave == 'importarpdfs'): executarImportarPDFs = True
            elif (comandoChave == 'gerarpdf'):
                executarGerarPDF = True
                nomeEvento = comandoValor
            elif (comandoChave == 'gerarevento'): executarGerarEvento = True
            elif (comandoChave == 'fazerbackup'): executarFazerBackup = True
            else: ajuda()
        if (executarImportarLattes): importarLattes(lattes, armazenamento)
        elif (executarImportarPDFs): importarPDFs(origem, destino)
        elif (executarGerarPDF): gerarPDF(destino, assinatura, tmp, nomeEvento)
        elif (executarGerarEvento): gerarEvento(str(uuid.uuid4()), datetime.today())
        elif (executarFazerBackup): fazerBackup(pgpass, 'localhost', '5432', 'acpc', 'acpc', datetime.today(), backup)
        else: ajuda()
    else: ajuda()
    if os.path.exists(tmp): shutil.rmtree(tmp)
    print('fim')

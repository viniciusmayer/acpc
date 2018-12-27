import glob, psycopg2, shutil, os

from PyPDF2 import PdfFileReader


class ImportarPDFsService(object):

    def __init__(self, destino):
        if not os.path.exists(destino): os.makedirs(destino)
        self.connection = psycopg2.connect("dbname='acpc' user='acpc' host='localhost' password='v1n1c1u5'")
        self.cursor = self.connection.cursor()

    def processar(self, origem, destino):
        for arquivo in glob.iglob(origem + '**/*.pdf', recursive=True):
            pdfFile = PdfFileReader(open(arquivo, 'rb'))
            if not pdfFile.isEncrypted:
                numeroPaginas = pdfFile.getNumPages()
                nomeArquivoOrigem = arquivo[arquivo.rfind('/') + 1:len(arquivo)] 
                select = 'SELECT id FROM public.trabalhos_arquivo where arquivo = \'{0}\''.format(nomeArquivoOrigem)
                self.cursor.execute(select)
                if (self.cursor.rowcount == 0):
                    shutil.copy2(arquivo, destino)
                    insert = 'INSERT INTO public.trabalhos_arquivo(arquivo, paginas, ativo) VALUES (\'{0}\', {1}, true)'.format(nomeArquivoOrigem, numeroPaginas)
                    self.cursor.execute(insert)
                    self.connection.commit()
                    print('arquivo inserido: {0}'.format(nomeArquivoOrigem))
                else:
                    print('arquivo ignorado: {0}'.format(nomeArquivoOrigem))
            else:
                print('arquivo ignorado: {0}'.format(nomeArquivoOrigem))

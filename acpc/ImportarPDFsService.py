import glob, sys, uuid, psycopg2, shutil, os

from PyPDF2 import PdfFileReader


class ImportarPDFsService(object):

    def __init__(self):
        self.conn = psycopg2.connect("dbname='acpc' user='acpc' host='localhost' password='v1n1c1u5'")
        self.cursor = self.conn.cursor()
        self.arquivos = {}
        self.paginas = 0

    def processar(self, origem, destino):
        if not os.path.exists(destino):
            os.makedirs(destino)
        for arquivo in glob.iglob(origem + '**/*.pdf', recursive=True):
            pdfFile = PdfFileReader(open(arquivo, 'rb'))
            if not pdfFile.isEncrypted:
                numeroPaginas = pdfFile.getNumPages()
                self.paginas += numeroPaginas 
                self.arquivos[arquivo] = pdfFile
                nomeArquivoOrigem = arquivo[arquivo.rfind('/') + 1:len(arquivo)] 
                nomeArquivoDestino = '{0}{1}'.format(destino, nomeArquivoOrigem)
                select = 'SELECT id FROM public.trabalhos_arquivo where arquivo = \'{0}\''.format(nomeArquivoDestino)
                self.cursor.execute(select)
                if (self.cursor.rowcount == 0):
                    shutil.copy2(arquivo, destino)
                    insert = 'INSERT INTO public.trabalhos_arquivo(arquivo, paginas) VALUES (\'{0}\', {1})'.format(nomeArquivoDestino, numeroPaginas)
                    self.cursor.execute(insert)
                    self.conn.commit()
                    print('file inserted: {0}'.format(nomeArquivoDestino))
                else:
                    print('file NOT inserted: {0}'.format(nomeArquivoDestino))

import glob, uuid, os, psycopg2

from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.lib.colors import Color
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


class GerarPDFService(object):

    def __init__(self, origem, tmp):
        self.connection = psycopg2.connect("dbname='acpc' user='acpc' host='localhost' password='v1n1c1u5'")
        self.cursor = self.connection.cursor()
        if not os.path.exists(tmp): os.makedirs(tmp)
        self.arquivos = {}
        for arquivo in glob.iglob(origem + '**/*.pdf', recursive=True):
            pdfFile = PdfFileReader(open(arquivo, 'rb'))
            nomeArquivoOrigem = arquivo[arquivo.rfind('/') + 1:len(arquivo)] 
            self.arquivos[nomeArquivoOrigem] = pdfFile

    def gerarCabecalho(self, largura, altura, pagina, numeroPaginas, assinatura, tmp):
        arquivo = '{0}{1}'.format(tmp, str(uuid.uuid4()))
        c = canvas.Canvas(arquivo, pagesize=(largura, altura))

        # fundo da paginacao
        color = Color(255, 255, 255, alpha=0)
        c.setFillColor(color)
        c.setStrokeColor(color)
        c.rect(largura - (2.5 * cm), altura - (1.1 * cm), (1.9 * cm), (0.5 * cm), fill=1)
        # paginacao
        c.setFillColor(Color(0, 0, 0, alpha=1))
        c.drawRightString(largura - (0.75 * cm), altura - (1 * cm), '{0}/{1}'.format(pagina, numeroPaginas))
        
        # fundo da assinatura
        #color = Color(255, 255, 255, alpha=0.5)
        #c.setFillColor(color)
        #c.setStrokeColor(color)
        #c.rect(largura - (2 * cm), (0.5 * cm), (1.5 * cm), (1.5 * cm), fill=1)
        # assinatura
        c.setFillColor(Color(0, 0, 0, alpha=1))
        c.drawImage(assinatura, largura - (2 * cm), (0.5 * cm), width=(1.5 * cm), height=(1.5 * cm))
        
        # gerar pagina
        c.showPage()
        c.save()
        cabecalho = PdfFileReader(open(arquivo, 'rb'))
        return cabecalho.getPage(0)

    def processar(self, assinatura, tmp, nomeEvento):
        selectEventoQuandoENumeroPaginas = 'select e.id, e.nome, e.quando, sum(a.paginas) \
                                            from public.trabalhos_eventotrabalho et \
                                                inner join public.trabalhos_evento e on e.id=et.evento_id \
                                                    {0} \
                                                inner join public.trabalhos_trabalho t on t.id=et.trabalho_id \
                                                inner join public.trabalhos_arquivo a on a.id=t.arquivo_id \
                                            group by e.id, e.nome, e.quando'
        if (nomeEvento is not None): selectEventoQuandoENumeroPaginas = selectEventoQuandoENumeroPaginas.format('and e.nome = \'{0}\''.format(nomeEvento))
        else: selectEventoQuandoENumeroPaginas = selectEventoQuandoENumeroPaginas.format('and 1=1')
        self.cursor.execute(selectEventoQuandoENumeroPaginas)
        rows = self.cursor.fetchall()
        for row in rows:
            numeroPaginas = row[3]
            numeroPaginaCabecalho = 1
            _arquivoDestino = PdfFileWriter()
            selectArquivos = 'select a.arquivo \
                                from public.trabalhos_eventotrabalho et \
                                    inner join public.trabalhos_evento e on e.id=et.evento_id and e.id = {0} \
                                    inner join public.trabalhos_trabalho t on t.id=et.trabalho_id \
                                    inner join public.trabalhos_arquivo a on a.id=t.arquivo_id \
                                order by et.ordem asc'.format(row[0])
            self.cursor.execute(selectArquivos)
            _rows = self.cursor.fetchall()
            for _row in _rows:
                nomeArquivo = _row[0]
                arquivo = self.arquivos[nomeArquivo]
                for numeroPagina in range(0, arquivo.getNumPages()):
                    pagina = arquivo.getPage(numeroPagina)
                    largura = float(pagina.mediaBox.getWidth())
                    altura = float(pagina.mediaBox.getHeight())
                    paginaCabecalho = self.gerarCabecalho(largura, altura, numeroPaginaCabecalho, numeroPaginas, assinatura, tmp)
                    pagina.mergePage(paginaCabecalho)
                    _arquivoDestino.addPage(pagina)
                    print('pagina gerada: {0}/{1}'.format(numeroPaginaCabecalho, numeroPaginas))
                    numeroPaginaCabecalho += 1
            nome = '{0}-{1}.{2}'.format(row[1], row[2], 'pdf')
            with open(nome, 'wb') as f:
                _arquivoDestino.write(f)
                print('arquivo gerado: {0}'.format(nome))

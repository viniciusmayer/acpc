import glob, uuid, os, psycopg2

from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.lib.colors import Color
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas


class GerarPDFService(object):

    def __init__(self, origem, tmp):
        self.conn = psycopg2.connect("dbname='acpc' user='acpc' host='localhost' password='v1n1c1u5'")
        self.cursor = self.conn.cursor()
        if not os.path.exists(tmp):
            os.makedirs(tmp)
        self.arquivos = {}
        for arquivo in glob.iglob(origem + '**/*.pdf', recursive=True):
            pdfFile = PdfFileReader(open(arquivo, 'rb'))
            if not pdfFile.isEncrypted:
                nomeArquivoOrigem = arquivo[arquivo.rfind('/') + 1:len(arquivo)] 
                self.arquivos[nomeArquivoOrigem] = pdfFile

    def gerarCabecalho(self, largura, altura, pagina, assinatura, tmp, numeroPaginas):
        arquivo = '{0}{1}'.format(tmp, str(uuid.uuid4()))
        c = canvas.Canvas(arquivo, pagesize=(largura, altura))
        # fundo da paginacao
        color = Color(255, 255, 255, alpha=0.5)
        c.setFillColor(color)
        c.setStrokeColor(color)
        c.rect(largura - (2.5 * cm), altura - (1.1 * cm), (1.9 * cm), (0.5 * cm), fill=1)
        # paginacao
        c.setFillColor(Color(0, 0, 0, alpha=1))
        c.drawRightString(largura - (0.75 * cm), altura - (1 * cm), '{0}/{1}'.format(pagina, numeroPaginas))
        # assinatura
        c.drawImage(assinatura, largura - (2 * cm), 0, width=(2 * cm), height=(2 * cm))
        # gerar pagina
        c.showPage()
        c.save()
        cabecalho = PdfFileReader(open(arquivo, 'rb'))
        return cabecalho.getPage(0)

    def processar(self, assinatura, tmp):
        selectEventoENumeroPaginas = 'select e.id, e.nome, sum(a.paginas) \
                                from public.trabalhos_eventotrabalho et \
                                    inner join public.trabalhos_evento e on e.id=et.evento_id \
                                    inner join public.trabalhos_trabalho t on t.id=et.trabalho_id \
                                    inner join public.trabalhos_arquivo a on a.id=t.arquivo_id \
                                group by e.id, e.nome'
        self.cursor.execute(selectEventoENumeroPaginas)
        rows = self.cursor.fetchall()
        for row in rows:
            idEvento = row[0]
            nomeEvento = row[1]
            numeroPaginas = row[2]
            numeroPaginaCabecalho = 1
            _arquivoDestino = PdfFileWriter()
            selectNomeEArquivos = 'select e.nome, a.arquivo \
                        from public.trabalhos_eventotrabalho et \
                            inner join public.trabalhos_evento e on e.id=et.evento_id and e.id = {0} \
                            inner join public.trabalhos_trabalho t on t.id=et.trabalho_id \
                            inner join public.trabalhos_arquivo a on a.id=t.arquivo_id \
                        order by et.ordem asc'.format(idEvento)
            self.cursor.execute(selectNomeEArquivos)
            _rows = self.cursor.fetchall()
            for _row in _rows:
                nomeArquivo = _row[1]
                arquivo = self.arquivos[nomeArquivo]
                for numeroPagina in range(0, arquivo.getNumPages()):
                    pagina = arquivo.getPage(numeroPagina)
                    largura = float(pagina.mediaBox.getWidth())
                    altura = float(pagina.mediaBox.getHeight())
                    paginaCabecalho = self.gerarCabecalho(largura, altura, numeroPaginaCabecalho, assinatura, tmp, numeroPaginas)
                    pagina.mergePage(paginaCabecalho)
                    _arquivoDestino.addPage(pagina)
                    print('pagina gerada: {0}/{1}'.format(numeroPaginaCabecalho, numeroPaginas))
                    numeroPaginaCabecalho += 1
            with open('{0}.{1}'.format(nomeEvento, 'pdf'), 'wb') as f:
                _arquivoDestino.write(f)

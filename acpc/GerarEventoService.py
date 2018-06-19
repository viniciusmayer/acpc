import psycopg2


class GerarEventoService(object):

    def __init__(self):
        self.conn = psycopg2.connect("dbname='acpc' user='acpc' host='localhost' password='v1n1c1u5'")
        self.cursor = self.conn.cursor()
    
    def processar(self, nome, quando):
        insertEvento = 'INSERT INTO public.trabalhos_evento(nome, quando) VALUES (\'{0}\', \'{1}\')'.format(nome, quando.strftime('%Y-%m-%d'))
        self.cursor.execute(insertEvento)
        self.conn.commit()
        print('evento inserido: {0}, {1}'.format(nome, quando.strftime('%Y-%m-%d')))
                
        selectEvento = 'SELECT id FROM public.trabalhos_evento where nome = \'{0}\' and quando = \'{1}\''.format(nome, quando.strftime('%Y-%m-%d'))
        insertEventoTrabalho = 'INSERT INTO public.trabalhos_eventotrabalho(ordem, evento_id, trabalho_id) \
                                    VALUES ({0}, ({1}), {2})'
        selectTrabalhos = 'select t.id from public.trabalhos_trabalho t \
                                inner join public.trabalhos_tag ta on ta.id=t.tag_id \
                            order by ta.ordem asc, t.ano desc, t.ano_fim desc, t.titulo asc'
        self.cursor.execute(selectTrabalhos)
        rows = self.cursor.fetchall()
        ordem = 0
        for row in rows:
            idTrabalho = row[0]
            self.cursor.execute(insertEventoTrabalho.format(ordem, selectEvento, idTrabalho))
            self.conn.commit()
            print('eventoTrabalho inserido: {0}, {1}, {2}'.format(ordem, '-idEvento-', idTrabalho))
            ordem += 1
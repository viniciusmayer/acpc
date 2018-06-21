import gzip
import os
import subprocess


class FazerBackupService(object):

    def __init__(self, pgpass, maquina, porta, banco, usuario, quando):
        self.pgpass, self.maquina, self.porta, self.banco, self.usuario, self.quando = pgpass, maquina, porta, banco, usuario, quando 
        self.arquivo = '{b}-{q}.gz'.format(b=banco, q=quando.strftime('%Y-%m-%d'))

    def processar(self):
        os.putenv('PGPASSFILE', self.pgpass)
        h = '--host={0}'.format(self.maquina)
        p = '--port={0}'.format(self.porta)
        d = '--dbname={0}'.format(self.banco)
        u = '--username={0}'.format(self.usuario)
        with gzip.open(self.arquivo, 'wb') as f:
            popen = subprocess.Popen(['pg_dump', '--no-password', h, p, d, u], stdout=subprocess.PIPE, universal_newlines=True)
            for stdout_line in iter(popen.stdout.readline, ''):
                f.write(stdout_line.encode('utf-8'))
            popen.stdout.close()
            popen.wait()
        os.unsetenv('PGPASSFILE')

    '''
    metodos possiveis de se fazer dump de um banco de dados (postgres) com python.
    '''

    def processarb(self):
        from sh import pg_dump
        os.putenv('PGPASSFILE', self.pgpass)
        h = '--host={0}'.format(self.maquina)
        p = '--port={0}'.format(self.porta)
        d = '--dbname={0}'.format(self.banco)
        u = '--username={0}'.format(self.usuario)
        with gzip.open(self.arquivo, 'wb') as f:
            pg_dump('--no-password', h, p, d, u, _out=f)
        os.unsetenv('PGPASSFILE')
        
    def processarc(self):
        import delegator
        comando = 'PGPASSFILE={pg} pg_dump --no-password --host={h} --port={p} --dbname={d} --username={u}'.format(pg=self.pgpass
                                                                                                                   , h=self.maquina
                                                                                                                   , p=self.porta
                                                                                                                   , d=self.banco
                                                                                                                   , u=self.usuario)
        with gzip.open(self.arquivo, 'wb') as f:
            c = delegator.run(comando)
            f.write(c.out.encode('utf-8'))
    
    def processard(self):
        import pexpect
        os.putenv('PGPASSFILE', self.pgpass)
        comando = 'pg_dump --no-password --host={h} --port={p} --dbname={d} --username={u}'.format(h=self.maquina
                                                                                                   , p=self.porta
                                                                                                   , d=self.banco
                                                                                                   , u=self.usuario)
        with gzip.open(self.arquivo, 'wb') as f:
            c = pexpect.spawn(comando)
            f.write(c.read())
        os.unsetenv('PGPASSFILE')
    
    def processare(self):
        comando = 'PGPASSFILE={pg} pg_dump --no-password --host={h} --port={p} --dbname={d} --username={u} | gzip > {a}'.format(pg=self.pgpass
                                                                                                                                , h=self.maquina
                                                                                                                                , p=self.porta
                                                                                                                                , d=self.banco
                                                                                                                                , u=self.usuario
                                                                                                                                , a=self.arquivo)
        os.system(comando)

class Trabalho(object):
    
    def __init__(self, id, ano, titulo):
        self.id = id
        self.ano = ano
        self.titulo = titulo
    
    def imprimir(self):
        print('id: {0}, ano: {1}, titulo: {2}'.format(self.id, self.ano, self.titulo))
    
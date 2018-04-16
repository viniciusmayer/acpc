class Trabalho(object):
    
    def __init__(self, numero, ano, titulo):
        self.numero = numero
        self.ano = ano
        self.titulo = titulo
    
    def imprimir(self):
        print('{0}. ano: {1}, titulo: {2}'.format(self.numero, self.ano, self.titulo))
    
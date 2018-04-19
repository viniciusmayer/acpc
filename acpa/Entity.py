class Trabalho(object):
    
    def __init__(self, titulo, ano, natureza, numero=None):
        self.ano = ano
        self.titulo = titulo
        self.natureza = natureza
        self.numero = numero
    
    def imprimir(self):
        print('\nid:{0} \ntitulo: {1} \nano: {2} \nnatureza:{3}'.format(self.numero, self.titulo, self.ano, self.natureza))

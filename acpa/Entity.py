class Trabalho(object):
    
    def __init__(self, numero, ano, titulo, natureza):
        self.numero = numero
        self.ano = ano
        self.titulo = titulo
        self.natureza = natureza
    
    def imprimir(self):
        print('\n{0}\nnatureza:{1}\nano: {2}\ntitulo: {3}'.format(self.numero, self.natureza, self.ano, self.titulo))

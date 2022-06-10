import re

class Produto:
    def __init__(self, sku, saldo, marca, data = 'Prazo definido pelo fabricante'):
        self.sku = sku
        self.saldo = saldo
        self.marca = marca
        self.data = data

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, valor):
        try:
            if isinstance(valor, float):
                self._saldo = valor
            else:
                self._saldo = float(0)
        except:
            print("error")

    @property
    def sku(self):
        return self._sku
    
    @sku.setter
    def sku(self, valor):
        try:
            if type(valor) == str:
                self._sku = valor
            else:
                self._sku = 'valornaoencontrado'
        except:
            print("error")

    @property
    def marca(self):
        return self._marca

    @marca.setter
    def marca(self, valor):
        try:
            if type(valor) == str:
                self._marca = valor
            else:
                self.__marca = 'valornaoencontrado'
        except:
            print("error")

        


     
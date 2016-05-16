#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import unittest

AbsoluteError, RelativeError = range(1,3)

class MethodException(Exception):
    def __init__(self, msg): self.msg = msg

class MaxIterReached(StopIteration):
    """Iteração máxima atingida"""
    def __init__(self, iter_max):
        print 'Iteração máxima atingida após {} iterações'.format(iter_max)

class MaxErrorReached(StopIteration):
    """Error máximo atingido"""
    def __init__(self, error_max):
        print 'Erro máximo {} atingido'.format(error_max)

class FoundSolution(StopIteration):
    """Solução encontrada"""
    def __init__(self, x):
        print 'Solução encontrada: %f'.format(x)

class NoConvergence(MethodException):
    """Função não convergente"""
    def __init__(self):
        super(MethodException, self).__init__("Função não converge usando o método de Newton")

class Newton:
    """Método de Newton"""
    def __init__(self, f, df, x0, erro_max, iter_max, err_type, casas_decimais=5):
        self.f = f # função
        self.df = df # função derivada
        self.x0 = round(x0, casas_decimais) # ponto inicial
        self.erro_max = erro_max # erro máximo
        self.iter_max = iter_max # nº de iterações máximas
        self.err_type = err_type # tipo de erro 
        self.casas_decimais = casas_decimais # nº de casas decimais
        self.iter_atual = 0 # iteração actual
        # verificar condições de convergência
        if not self.converges(): # se não passar os testes de convergência
            raise NoConvergence() # levanta uma excepção

    def __str__(self):
        return '''
        Ponto inicial: {}
        Error máximo: {}
        Iteração atual: {}
        Iteração máxima: {}
        Tipo de Erro: {}
        '''.format(self.x0, self.erro_max, self.iter_atual, self.iter_max, self.error_str())

    def error_str(self):
        return 'Absoluto' if self.err_type == AbsoluteError else 'Relativo'

    def __iter__(self):
        return self

    # TODO
    def converges(self):
        """Verifica se a função converge"""
        return True

    def next(self):
        """Generates a row of results"""
        if self.iter_atual == 0:
            fxk = round(self.f(self.x0), self.casas_decimais)
            dfxk = round(self.df(self.x0), self.casas_decimais)
            xk = round(self.x0 - (fxk / dfxk), self.casas_decimais)
            resultados = (self.iter_atual, self.x0, self.f(self.x0), self.df(self.x0), xk, None)
            self.xk = xk
            self.iter_atual += 1
            return resultados 
        else:
            if self.iter_atual == self.iter_max: raise MaxIterReached(self.iter_max)
            x_prev = self.xk
            fxk = round(self.f(self.xk), self.casas_decimais)
            dfxk = round(self.df(self.xk), self.casas_decimais)
            xk = round(self.xk - (fxk / dfxk), self.casas_decimais)
            erro = round(self.erro(x_prev, xk), self.casas_decimais)
            resultados = (self.iter_atual, x_prev, fxk, dfxk, xk, erro)
            if xk == 0.0: raise FoundSolution(xk)
            if erro <= self.erro_max: raise MaxErrorReached(self.erro_max) 
            self.x0 = xk
            self.iter_atual += 1
            return resultados
        
    # TODO: test
    def iters(self, n):
        """Returns the first n rows of results"""
        return [row for row in self]

    def erro(self, xk0, xk1):
        """xk1 => xk e xk0 => xk-1"""
        if self.err_type == AbsoluteError:
            return abs(xk1 - xk0)
        elif self.err_type == RelativeError:
            return (abs(xk1 - xk0) / max(1, abs(xk0)))

class TestErrors(unittest.TestCase):
    def test(self):
        self.assertEqual(1,1)

if __name__ == '__main__':
    #unittest.main()
    f = lambda x: (x**4) + x - 1
    df = lambda x: 4*(x**3) + 1
    try:
        n = Newton(f=f, df=df, x0=2.5, erro_max=0.001, iter_max=5, err_type=AbsoluteError, casas_decimais=5)
        print(n)
        print 'k\txk\tfxk\tdfxk\terro'
        for k in n: # first 10 iterations
            print(k)
    except MethodException as e:
        print(e)


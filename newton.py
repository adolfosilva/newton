#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""Implementação do método iterativo de Newton-Raphson."""

import random
from sympy import sympify

# Erro absoluto e relativo
AbsoluteError, RelativeError = range(1, 3)

class Newton(object):
    """Método de Newton"""
    def __iter__(self): return self

    def __init__(self, f, intervalo, erro_max, iter_max, err_type, casas_decimais):
        self.f = sympify(f).as_poly() # função
        self.intervalo = intervalo # intervalo
        self.df = self.f.diff() # primeira derivada
        self.ddf = self.df.diff() # segunda derivada
        self.x0 = self.choose_initial_guess() # ponto inicial
        self.erro_max = erro_max # erro máximo
        self.iter_max = iter_max # nº de iterações máximas
        self.err_type = err_type # tipo de erro
        self.casas_decimais = casas_decimais # nº de casas decimais
        self.iter_atual = 0 # iteração actual
        # verificar condições de convergência
        if not self.converges(): # se não passar os testes de convergência
            raise Exception('Função não converge usando o método de Newton.') # levanta uma excepção

    def __str__(self):
        return '''
        Função: {}
        Primeira derivada: {}
        Segunda derivada: {}
        Intervalo inicial: {}
        Ponto inicial: {}
        Error máximo: {}
        Iteração atual: {}
        Iteração máxima: {}
        Tipo de Erro: {}
        '''.format(self.f, self.df, self.ddf, self.intervalo, self.x0, self.erro_max, self.iter_atual, self.iter_max, self.error_str())

    def error_str(self):
        """Retorna uma representação textual do tipo de erro"""
        return 'Absoluto' if self.err_type == AbsoluteError else 'Relativo'

    def converges(self):
        """Verifica se a função converge."""
        a, b = self.intervalo
        if self.f(a) * self.f(b) >= 0.0: return False
        return True

    def choose_initial_guess(self):
        """Escolhe o ponto inicial."""
        a, b = self.intervalo
        if self.f(a) * self.ddf(a) > 0.0: # testa ponto a
            return a
        if self.f(b) * self.ddf(b) > 0.0: # testa ponto b
            return b
        c = round(random.uniform(a, b), 1) # ponto aleatório entre a e b, com uma casa decimal
        while self.f(c) * self.ddf(c) <= 0.0:
            c = round(random.uniform(a, b), 1)
        return c

    def error(self, xk0, xk1):
        """Calcula o erro para uma determinada iteração.
        xk1 => xk
        xk0 => xk-1"""
        if self.err_type == AbsoluteError:
            return abs(xk1 - xk0)
        elif self.err_type == RelativeError:
            return abs(xk1 - xk0) / max(1, abs(xk0))

    def next(self):
        """Retorna uma linha de resultados."""
        if self.iter_atual == 0:
            fxk = round(self.f(self.x0), self.casas_decimais)
            dfxk = round(self.df(self.x0), self.casas_decimais)
            xk = round(self.x0 - (fxk / dfxk), self.casas_decimais)
            resultados = (self.iter_atual, self.x0, fxk, dfxk, xk, None)
            self.xk = xk
            self.iter_atual += 1
            return resultados
        else:
            if self.iter_atual == self.iter_max: raise Exception('Iteração máxima atingida após {} iterações.'.format(self.iter_max))
            x_prev = self.xk
            fxk = round(self.f(self.xk), self.casas_decimais)
            dfxk = round(self.df(self.xk), self.casas_decimais)
            xk = round(self.xk - (fxk / dfxk), self.casas_decimais)
            erro = round(self.error(x_prev, xk), self.casas_decimais)
            resultados = (self.iter_atual, x_prev, fxk, dfxk, xk, erro)
            if xk == 0.0: raise Exception('Solução encontrada: %f'.format(xk))
            if erro <= self.erro_max: raise Exception('Erro máximo {} atingido.'.format(self.erro_max))
            self.xk = xk
            self.iter_atual += 1
            return resultados

    def iters(self, n):
        """Retorna as primeiras n linhas de resultados."""
        return [self.next() for _ in range(n)]

if __name__ == '__main__':
    try:
        n = Newton(f="x**4 + x - 1", intervalo=(0.0, 1.0), erro_max=1e-10, iter_max=100, err_type=AbsoluteError, casas_decimais=100)
        print n # debug
        print 'k\txk\tf(xk)\tdf(xk)\txk+1\terro'
        for k in n:
            print k
    except Exception as e:
        print e

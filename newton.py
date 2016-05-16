#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import unittest
import random
import sympy

# Erro absoluto e relativo
AbsoluteError, RelativeError = range(1,3)

class MethodException(Exception):
    def __init__(self, msg): self.msg = msg

class MaxIterReached(StopIteration):
    """Iteração máxima atingida"""
    def __init__(self, iter_max):
        print 'Iteração máxima atingida após {} iterações.'.format(iter_max)

class MaxErrorReached(StopIteration):
    """Error máximo atingido"""
    def __init__(self, error_max):
        print 'Erro máximo {} atingido.'.format(error_max)

class FoundSolution(StopIteration):
    """Solução encontrada"""
    def __init__(self, x):
        print 'Solução encontrada: %f'.format(x)

class NoConvergence(MethodException):
    """Função não convergente"""
    def __init__(self):
        super(MethodException, self).__init__("Função não converge usando o método de Newton.")

class Newton:
    """Método de Newton"""
    def __init__(self, f, intervalo, erro_max, iter_max, err_type, casas_decimais=5):
        self.f = f # função
        self.intervalo = intervalo # intervalo
        self.df = f.diff() # primeira derivada
        self.ddf = self.df.diff() # segunda derivada
        self.x0 = self.choose_initial_guess() # ponto inicial
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
        Função: {}
        Primeira derivada: {}
        Segunda derivada: {}
        Intervalo inicial: {}
        Ponto inicial: {}
        Error máximo: {}
        Iteração atual: {}
        Iteração máxima: {}
        Tipo de Erro: {}
        '''.format(self.f, self.df, self.ddf, self.intervalo, self.x0, self.erro_max,
                self.iter_atual, self.iter_max, self.error_str())

    def error_str(self):
        return 'Absoluto' if self.err_type == AbsoluteError else 'Relativo'

    def __iter__(self): return self

    # TODO: implement
    def converges(self):
        """Verifica se a função converge."""
        return True

    def choose_initial_guess(self):
        """Escolhe o ponto inicial."""
        x = sympy.symbols('x')
        a, b = self.intervalo
        if self.f.evalf(subs={x: a}) * self.ddf.evalf(subs={x: a}) > 0.0: # testa ponto a
            return a
        if self.f.evalf(subs={x: b}) * self.ddf.evalf(subs={x: b}) > 0.0: # testa ponto b
            return b
        c = round(random.uniform(a,b), 1) # ponto aleatório entre a e b, com uma casa decimal
        while self.f.evalf(subs={x: c}) * self.ddf.evalf(subs={x: c}) <= 0.0:
            c = round(random.uniform(a,b), 1)
        return c

    def error(self, xk0, xk1):
        """Calcula o erro para uma determinada iteração.
        xk1 => xk
        xk0 => xk-1"""
        if self.err_type == AbsoluteError:
            return abs(xk1 - xk0)
        elif self.err_type == RelativeError:
            return (abs(xk1 - xk0) / max(1, abs(xk0)))

    # TODO: get rid of if...else
    def next(self):
        x = sympy.symbols('x')
        if self.iter_atual == 0:
            fxk = round(self.f.evalf(subs={x: self.x0}), self.casas_decimais)
            dfxk = round(self.df.evalf(subs={x: self.x0}), self.casas_decimais)
            xk = round(self.x0 - (fxk / dfxk), self.casas_decimais)
            resultados = (self.iter_atual, self.x0, fxk, dfxk, xk, None)
            self.xk = xk
            self.iter_atual += 1
            return resultados 
        else:
            if self.iter_atual == self.iter_max: raise MaxIterReached(self.iter_max)
            x_prev = self.xk
            fxk = round(self.f.evalf(subs={x: self.xk}), self.casas_decimais)
            dfxk = round(self.df.evalf(subs={x: self.xk}), self.casas_decimais)
            xk = round(self.xk - (fxk / dfxk), self.casas_decimais)
            erro = round(self.error(x_prev, xk), self.casas_decimais)
            resultados = (self.iter_atual, x_prev, fxk, dfxk, xk, erro)
            if xk == 0.0: raise FoundSolution(xk)
            if erro <= self.erro_max: raise MaxErrorReached(self.erro_max) 
            self.xk = xk
            self.iter_atual += 1
            return resultados
        
    # TODO: test
    def iters(self, n):
        """Retorna as primeiras n linhas de resultados."""
        return [self.next() for _ in range(n)]

class TestErrors(unittest.TestCase):
    f1 = sympy.sympify("x**4 + x - 1")

    def test_initial_guess(self):
        n = Newton(f=self.f1, intervalo=(0.0,1.0), erro_max=0.0005, iter_max=3, err_type=RelativeError, casas_decimais=4)
        self.assertEqual(n.choose_initial_guess(), 1.0)

    def test_max_error(self):
        n = Newton(f=self.f1, intervalo=(0.0,1.0), erro_max=0.001, iter_max=5, err_type=RelativeError, casas_decimais=4)
        self.assertEqual((0,1.0,1.0,5.0,0.8,None), n.next())
        self.assertEqual((1,0.8,0.2096,3.048,0.7312,0.0688), n.next())
        self.assertEqual((2,0.7312,0.0171,2.5638,0.7245,0.0067), n.next())
        with self.assertRaises(MaxErrorReached): n.next()

    def test_max_iter(self):
        n = Newton(f=self.f1, intervalo=(0.0,1.0), erro_max=0.0005, iter_max=3, err_type=RelativeError, casas_decimais=4)
        self.assertEqual((0,1.0,1.0,5.0,0.8,None), n.next())
        self.assertEqual((1,0.8,0.2096,3.048,0.7312,0.0688), n.next())
        self.assertEqual((2,0.7312,0.0171,2.5638,0.7245,0.0067), n.next())
        with self.assertRaises(MaxIterReached): n.next()

    def test_iters(self):
        from copy import copy
        n = Newton(f=self.f1, intervalo=(0.0,1.0), erro_max=0.0005, iter_max=3, err_type=RelativeError, casas_decimais=4)
        n0, n1, n2, n3 = copy(n), copy(n), copy(n), copy(n)
        self.assertEqual([], n1.iters(0))
        self.assertEqual([(0,1.0,1.0,5.0,0.8,None)], n1.iters(1))
        self.assertEqual([(0,1.0,1.0,5.0,0.8,None),(1,0.8,0.2096,3.048,0.7312,0.0688)], n2.iters(2))
        self.assertEqual([(0,1.0,1.0,5.0,0.8,None),(1,0.8,0.2096,3.048,0.7312,0.0688),(2, 0.7312, 0.0171, 2.5638, 0.7245, 0.0067)], n3.iters(3))


if __name__ == '__main__':
    # unittest.main()
    f = sympy.sympify("x**4 + x - 1")
    try:
        n = Newton(f=f, intervalo=(0.0,1.0), erro_max=1e-10, iter_max=100, err_type=AbsoluteError, casas_decimais=100)
        print(n) # debug
        print 'k\txk\tf(xk)\tdf(xk)\txk+1\terro'
        for k in n:
            print(k)
    except MethodException as e:
        print(e)

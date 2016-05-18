#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sympy
import unittest
import newton

class TestErrors(unittest.TestCase):
    f1 = "x**4 + x - 1"

    def test_initial_guess(self):
        n = newton.Newton(f=self.f1, intervalo=(0.0, 1.0), erro_max=0.0005, iter_max=3, err_type=newton.RelativeError, casas_decimais=4)
        self.assertEqual(n.choose_initial_guess(), 1.0)

    def test_max_error(self):
        n = newton.Newton(f=self.f1, intervalo=(0.0, 1.0), erro_max=0.001, iter_max=5, err_type=newton.RelativeError, casas_decimais=4)
        self.assertEqual((0, 1.0, 1.0, 5.0, 0.8, None), n.next())
        self.assertEqual((1, 0.8, 0.2096, 3.048, 0.7312, 0.0688), n.next())
        self.assertEqual((2, 0.7312, 0.0171, 2.5638, 0.7245, 0.0067), n.next())
        with self.assertRaises(newton.MaxErrorReached): n.next()

    def test_max_iter(self):
        n = newton.Newton(f=self.f1, intervalo=(0.0, 1.0), erro_max=0.0005, iter_max=3, err_type=newton.RelativeError, casas_decimais=4)
        self.assertEqual((0, 1.0, 1.0, 5.0, 0.8, None), n.next())
        self.assertEqual((1, 0.8, 0.2096, 3.048, 0.7312, 0.0688), n.next())
        self.assertEqual((2, 0.7312, 0.0171, 2.5638, 0.7245, 0.0067), n.next())
        with self.assertRaises(newton.MaxIterReached): n.next()

    def test_iters(self):
        from copy import copy
        n = newton.Newton(f=self.f1, intervalo=(0.0, 1.0), erro_max=0.0005, iter_max=3, err_type=newton.RelativeError, casas_decimais=4)
        n0, n1, n2, n3 = copy(n), copy(n), copy(n), copy(n)
        self.assertEqual([], n0.iters(0))
        self.assertEqual([(0, 1.0, 1.0, 5.0, 0.8, None)], n1.iters(1))
        self.assertEqual([(0, 1.0, 1.0, 5.0, 0.8, None), (1, 0.8, 0.2096, 3.048, 0.7312, 0.0688)], n2.iters(2))
        self.assertEqual([(0, 1.0, 1.0, 5.0, 0.8, None), (1, 0.8, 0.2096, 3.048, 0.7312, 0.0688), (2, 0.7312, 0.0171, 2.5638, 0.7245, 0.0067)], n3.iters(3))

if __name__ == '__main__':
    unittest.main()

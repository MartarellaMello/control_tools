"""
Codigo resposvael pela definicao e operacao da quesse Controle
"""
from control_tools.functions import *
import matplotlib.pyplot as plt
import sympy as sp
import numpy as np
import warnings

class Controle:
    # Variaveis globais da classe
    t = sp.Symbol('t')
    s = sp.Symbol('s')
    compensador = 1 / s
    def __init__(self, coef_n, coef_d, constraint=0) -> None:
        self._constraint = constraint

        ft = ft_s(coef_n, coef_d)
        self._ft = ft

    @property
    def ft(self):
        return self._ft["FT"]

    @property
    def c_contorno(self):
        return self._constraint

    @property
    def info(self):
        return self._ft

    @property
    def view(self):
        txt = self.info["FT"]
        print("LaTex", sp.latex(txt))

    def time_f(self, plot=True):
        ft = self.info["FT"]
        ft_n = ft_t(ft, 0, 50, plot)
        self.info["f_time"] = ft_n
        return ft_n

    def lugar_raizes(self, plot=False):
        r, k = locus_root(self.info["FT"], plot)
        return r, k

    def step(self, plot=False):
        s = sp.Symbol("s")
        self.info["FT"] = self.info["FT"] * (s ** (-1))

        ft_t = self.time_f(plot)
        ft_root = self.lugar_raizes(plot)
        self.info["step_Ans"] = ft_t
        self.info["Root_locus"] = ft_root

        return self.info


    def close_loop(self, compensador=1/s, plot=False):
        """
        Calcula o sistema de controle em malha fechada
        :param plot: Plota o grafico do sistema de controle em malha fechada
        :param compensador: Funcao de controlador.
        :return: Retorna a funcao de transferencia do sistema de controle em malha fechada
        """
        s = sp.Symbol('s')
        ft = self.info["FT"]
        ft_cl = (ft * compensador) / (1 + ft * compensador)

        self.info["FT_cl"] = ft_cl

        if plot:
            ft_t(ft_cl, 0, 50, plot)
            return ft_cl

        return ft_cl


class Compensador(Controle):
    """
    Classe que define o controlador de malha fechada
    """

    def __init__(self, coef_n, coef_d):
        super().__init__(coef_n, coef_d)
        self._ft = Controle(coef_n, coef_d)
    @property
    def ft(self):
        return self._ft.ft

    @property
    def info(self):
        return self._ft.info

    @property
    def view(self):
        """
        Exibe a funcao de transferencia do controlador
        :return: None
        """
        txt = self.ft.ft
        print("LaTex", sp.latex(txt))


if __name__ == '__main__':
    # Coef da funcao de transferencia
    n = (1, 4)
    d = (1, 5, 2)
    # Coeficiente do controlador
    nd = 21
    dc = 12

    ft = Controle(n, d)
    ft.time_f()
    ft.lugar_raizes(plot=False)
    ft.step(plot=False)

    h = Compensador(nd, dc)
    print("H(s) = ", h.ft)
    ft.close_loop(h.ft, plot=True)
# teste = ft.step()


# ft.time_function()
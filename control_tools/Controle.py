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
        transfer_function = ft_setter(coef_n, coef_d)

        self._ft = transfer_function

    @property
    def ft(self):
        return self._ft["FT"]

    @property
    def c_contorno(self):
        return self._constraint

    @property
    def info(self):
        return self._ft


    def step(self, plot=False):
        """
        Calcula a resposta ao degrau do sistema de controle
        :param plot: True se deseja plotar o grafico da resposta ao degrau
        :return: Retorna a resposta ao degrau do sistema de controle com ou sem o grafico. Alem disso, armazena a
        resposta ao degrau no dicionario info com a chave "step".
        """
        transfer_function = self.info["FT"]
        ft_n = ft_t(transfer_function, plot)
        self.info["step"] = ft_n
        return ft_n

    def lugar_raizes(self, plot=False):
        r, k = root_locus(self.info["FT"], plot)
        return r, k


    def close_loop(self, compensador, plot=False):
        """
        Calcula o sistema de controle em malha fechada
        :param plot: Plota o grafico do sistema de controle em malha fechada
        :param compensador: Funcao de controlador.
        :return: Retorna a funcao de transferencia do sistema de controle em malha fechada. Alem disso, armazena os
        resultados no dicionario info comas chaves "MF" -> funcao de transferencia para malha fechada e
        "MF_step" --> indica a resposta do sistema a um degral unitario.
         """
        c_loop = ct.feedback(self.ft, compensador)
        ft_cl = ft_t(c_loop, plot)
        self.info["MF"] = c_loop
        self.info["MF_step"] = ft_cl

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


if __name__ == '__main__':
    # Coef da funcao de transferencia
    n = 25,
    d = (1, 4 ,24)
    # Coeficiente do controlador
    nd = 21
    dc = 12

    ft = Controle(n, d)
    ft.step(plot=True)
    ft.lugar_raizes(plot=True)
    # ft.step(plot=False)

    # h = Compensador(nd, dc)
    # print("H(s) = ", h.ft)
    # ft.close_loop(h.ft, plot=True)
# teste = ft.step()


# ft.time_function()
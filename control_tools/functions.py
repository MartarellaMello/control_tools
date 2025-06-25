"""

Principais funcooes para problemas de controle

"""
from os import times, times_result
import numpy as np
import matplotlib.pyplot as plt
import warnings
import sympy as sp
import control as ct


def ft_setter(numerador: list, denominador: list) -> dict:
    """
    Retorna as informacoes da funcao de transferencia
    :param numerador: Coeficientes do numerador da funcao de transferencia
    :param denominador: Coeficientes do denominador da funcao de transferencia
    :return: Retorna um dicionario com as informacoes da funcao de transferencia.

    Formato do dicionario:
    return: dict
        {
        'FT': Funcao de transferencia,
        "Numerador": Coeficientes do numerador,
        "Denominador": Coeficientes do denominador,
        'Polos': Polos da funcao de transferencia,
        'Raiz': Raizes da funcao de transferencia
        }

    return['FT'] --> retorna a funcao de transferencia. O tipo de dado é control.TransferFunction
    return['Numerador'] --> Retorna os coeficientes do numerador da funcao de transferencia
    return['Denominador'] --> Retorna os coeficientes do denominador da funcao de transferencia
    return['Polos'] --> Retorna os polos da funcao de transferencia
    return['Raiz'] --> Retorna as raizes da funcao de transferencia
    """

    # Checa se o numerador e denominador sao listas
    if isinstance(numerador, tuple) or isinstance(denominador, tuple):
        numerador = list(numerador)
        denominador = list(denominador)

    polos = np.roots(list(numerador))  # Calcula os polos do numerador
    raiz = np.roots(list(denominador))
    wn = 0

    for i in raiz:
        wn += i ** 2

    ft = ct.TransferFunction(numerador, denominador)
    ft = {
        'FT': ft,
        "Numerador": numerador,
        "Denominador": denominador,
        'Polos': polos,
        'Raiz': raiz
    }
    return ft

def get_coef(ft) -> tuple:
    """
    Capta os coeficientes do numerador e do denominador da funcao de transferencia.
    :param ft:  A funcao de transferencia que se deseja obeter os coeficientes.
    :return: Retorina uma tupla com os calores dos coeficentes
    """
    s = sp.Symbol('s')
    n, d = sp.fraction(sp.simplify(ft))
    n = sp.Poly(n, s).all_coeffs()
    d = sp.Poly(d, s).all_coeffs()

    # Converte em lista os coeficientes do numerador e denominador
    coef_n = (float(c) for c in sp.Poly(n, s).all_coeffs())
    coef_d = (float(c) for c in sp.Poly(d, s).all_coeffs())
    return tuple(coef_n) ,tuple(coef_d)


def dirac_delta(x):
    # Aproximação: 1 se x==0, senão 0 (não é o correto matematicamente, mas pode servir)
    return np.where(np.isclose(x, 0), 1, 0)


def select(conds, choices, default=None):
    out = np.full(
        np.broadcast_shapes(*[np.shape(c) for c in choices if hasattr(c, 'shape')] + [np.shape(conds[0])]), default
    )
    for cond, choice in zip(conds, choices):
        np.copyto(out, choice, where=cond)
    return out


def ft_t(funcao_transferencia, plot=False):
    """
    :param funcao_transferencia: A funcao de transferencia G(s) type: control.TransferFunction
    :param plot: True ou False
    :return: Retorna a funcao matecamica  g(t) e plota o grafico da funcao

    """
    # Calcula a resposnta no tempo da funcao de transferencia....
    t, y = ct.step_response(funcao_transferencia)

    # Criando o Plot, caso seja solicitado pelo usuario
    if plot:
        # Plota o grafico da funcao de transferencia
        plt.plot(t, y)
        plt.xlabel('Tempo (s)')
        plt.ylabel('g(t)')
        plt.title(f'Resposta ao Degrau de {funcao_transferencia}')
        plt.grid(True)
        plt.show()
    else:
        return t, y

    return t, y

def root_locus(funcao_transferecia, plot=False) -> tuple or None:
    """
    Retorna o grafico do lugar das raizews para um funcao de transfecnia conhecida
    :param funcao_transferecia: Deve ser do tipo sympy ou control.TransferFunction
    :param plot: Se True, plota o grafico do lugar das raizes, caso contrario, retorna apenas os valores de r e k
    :return: None
    """
    r, k = ct.root_locus_map(funcao_transferecia)

    if plot:
        ct.root_locus_plot(funcao_transferecia)
        plt.title("Lugar das raízes (Root Locus)")
        plt.xlabel("Parte Real")
        plt.ylabel("Parte Imaginária")
        plt.grid(True)
        plt.show()

    return r, k




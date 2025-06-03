"""

Principais funcooes para problemas de controle

"""
from os import times, times_result

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import warnings
import sympy as sp
import control

def ft_s(numerador, denominador):
    # Variaveis simbolicas
    s = sp.Symbol('s')
    n = 0
    d = 0
    # Verificacao do denominador
    if denominador == 0:
        print('NAO SE PODE DIVIDIR POR ZERO!')
        return None

    else:
        n = sum(c * s ** (len(numerador) - i - 1) for i, c in enumerate(numerador))
        d = sum(c * s ** (len(denominador) - i - 1) for i, c in enumerate(denominador))


        # Deterinando os polos do sistema
        polos = sp.solve(n, s)

        raiz = sp.solve(d, s)
        wn = 0

        for i in raiz:
            wn += i ** 2

        ft = n * (d ** (-1))
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


def ft_t(funcao_transferencia, inicio=0, final=5, dt=200, plot=True):
    """
    :param funcao_transferencia: A funcao de transferencia G(s) em symbol
    :param inicio: O tempo de inicio da construcao do grafico
    :param final: Fim tempo de construcao do grafico
    :param dt: Espaacmento entre intervalo de dado
    :param plot: True ou False
    :return: Retorna a funcao matecamica  g(t) e plota o grafico da funcao

    """
    t = sp.Symbol('t')
    s = sp.Symbol('s')
    ft_n = sp.inverse_laplace_transform(funcao_transferencia, s ,t)
    time_values = np.linspace((inicio, final), dt, dtype=np.complex128)
    y = []
    x = []

    for i in time_values:
        comp = i[0] + i[1]
        y.append(ft_n.subs(t, comp))
        x.append(i)

    print(len(y))
    print(f"valores de y(t) da funcao F(s) = {ft_n}, implementados com sucesso")



    if plot:
        axis_size = x, y
        plt.plot(x, y, label=f'g(t) = {ft_n}')
        plt.xlabel('Tempo (s)')
        plt.ylabel('g(t)')
        plt.title(f'Funcao {funcao_transferencia}')
        plt.grid(True)
        plt.show()
    else:
        return time_values, y

    return time_values, y

def locus_root(funcao_transferecia, plot=False) -> tuple:
    """
    Retorna o grafico do lugar das raizews para um funcao de transfecnia conhecida
    :param coefs: Coeficientes da  Funcao de transferencia. Deve ser no do tipo tupla ou lista
    :return: None
    """

    # Defina s como símbolo único

    s = sp.symbols('s')
    # Simplifique e separe numerador e denominador
    # Calculo do lugar das raizes
    coef = get_coef(funcao_transferecia)

    margin = np.sqrt(sum(coef[1]))  # Adjust as needed
    x_min = margin - margin
    x_max = margin
    y_min = - margin
    y_max = 1


    # Verifica se o coeficiente é vazio ou nulo
    if not coef or coef[0] == 0 or coef[1] == 0:
        warnings.warn("A funcao de transferencia G(s) nao pode ser zero")
        return None

    # Cria a funcao de transferencia usando a biblioteca control
    ft_control = control.TransferFunction(coef[0], coef[1])
    print(f"Função de transferência: {ft_control}")
    # Plote o root locus
    if plot:
        rlist, klist = control.root_locus(ft_control, plot=True, xlim=(x_min, x_max), ylim=(y_min, y_max))
        plt.title("Lugar das raízes (Root Locus)")
        plt.xlabel("Parte Real")
        plt.ylabel("Parte Imaginária")
        plt.grid(True)
        plt.show()
    else:
        rlist, klist = control.root_locus(ft_control, plot=False)

    return rlist, klist




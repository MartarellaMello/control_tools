"""

Principais funcooes para problemas de controle

"""
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import warnings
import sympy as sp
import pydevd_pycharm
import control
import scipy
import scipy.special

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


def ft_t(funcao_transferencia, inicio=5, final=5, dt=550, plot=False):
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
    #ft_n = sp.lambdify(t, ft_n, modules=[{"DiracDelta": dirac_delta,
    #                                     "select": select}, 'numpy', 'scipy'])
    ft_n = sp.lambdify(t, ft_n, modules=['scipy'])

    time_values = np.linspace(inicio, final, dt, dtype=np.complex128)
    y = ft_n(time_values)

    if plot:
        plt.plot(time_values, y)
        plt.xlabel('Tempo (s)')
        plt.ylabel('g(t)')
        plt.title(f'Funcao {funcao_transferencia}')
        plt.grid(True)
        plt.show()
    else:
        return y
    return time_values, y


def locus_root(coefs, plot=False, xaxis_size=(-15, 5), yaxis_size=(-9, 9)) -> tuple:
    """
    Retorna o grafico do lugar das raizews para um funcao de transfecnia conhecida
    :param coefs: Coeficientes da  Funcao de transferencia. Deve ser no do tipo tupla ou lista
    :param xaxis_size: Determina o tamanho do eixo x
    :param yaxis_size: Determina o tamanho do eixo y
    :return: None
    """

    # Defina s como símbolo único

    s = sp.symbols('s')
    # Simplifique e separe numerador e denominador
    # Calculo do lugar das raizes

    ft_control = control.TransferFunction(coefs[0], coefs[1])

    print(f"Função de transferência: {ft_control}")
    # Plote o root locus
    if plot:
        rlist, klist = control.root_locus(ft_control, plot=True)
        plt.title("Lugar das raízes (Root Locus)")
        plt.xlabel("Parte Real")
        plt.ylabel("Parte Imaginária")
        plt.xlim(xaxis_size)
        plt.ylim(yaxis_size)

        plt.grid(True)
        plt.show()
    else:
        rlist, klist = control.root_locus(ft_control, plot=False)

    return rlist, klist


class Controle:

    # Variaveis globais da classe

    t = sp.Symbol('t')
    s = sp.Symbol('s')


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


    def time_function(self, plot=False):
        ft = self.info["FT"]
        ft_n = ft_t(ft, 0, 50, plot)
        return ft_n


    def lugar_raizes(self, plot=False):
        coefs = list(ft.info["Numerador"], ft.info["Denominador"])
        r, k = locus_root(coefs, plot)
        return r, k

    def step(self):
        s = sp.Symbol("s")
        self.info["FT"] = self.info["FT"] * (s ** (-1))

        ft_t  = self.time_function()
        ft_root =  self.ft.lugar_raizes()
        self.info["Time_Ans"] = ft_t
        self.info["Root_locus"] = ft_root

        return self.info

if __name__ == '__main__':
    n = (1, 4)
    d = (1, 5, 3, 2)

    ft = Controle(n, d)
    ft.time_function()
    ft.lugar_raizes()

    teste = ft.step()

    a = 2 + 3

    ft.time_function()
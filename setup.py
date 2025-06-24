from setuptools import setup, find_packages

setup(
    name="control_tools",  # Nome do pacote no PyPI
    version="0.2.22",  # Versão do seu pacote
    packages=find_packages(),  # Automaticamente encontra subpacotes
    install_requires=["sympy", "numpy", "matplotlib", "control", "setuptools"], # Dependências (ex: ["numpy"])
    author="Felipe Martarella de Souza Mello",
    author_email="d2020001214@unifei.edu.br",
    description="Pacote designado para solucao de problemas classico de controle.",
    #url="https://github.com/seuusuario/controls_tools",  # Opcional, ajuste para seu repositório
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
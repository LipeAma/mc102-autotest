""" Simulador de susy kk"""
# Primeiramente, certifique-se de que o arquivo susy.py esteja na mesma pasta que main.py
#
# Substitua 'meuprograma.py' com o nome do seu programa Ex: 'lab04.py'
#
# Substitua também o número 1 pelo número do seu exercício,
# ou seja, se estiver programando o laboratório 5, substitua 1 por 5.
#
# PS: Se quiser realizar um teste em específico, por exemplo, para realizar o teste 4 no exercício 5, use:
#     teste_unico('meuprograma.py', 5, 4)

# Ignore isso ---------------------------------
from os import chdir, path
chdir(path.normpath(path.dirname(__file__)))
from susy import testar_tudo, teste_unico
# ---------------------------------------------

# Altere aqui ---------------------------------
testar_tudo('meuprograma.py', 1)
# ---------------------------------------------

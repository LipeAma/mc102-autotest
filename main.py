""" Simulador de susy kk"""

# Primeiramente, certifique-se de que o arquivo susy.py esteja na mesma pasta que main.py
#
# Substitua 'C:/Users/aluno/Desktop/meuprograma.py' com o caminho completo para seu programa
#
# Se main.py estiver na mesma pasta que o seu programa, não será preciso indicar o caminho completo
# apenas o nome do programa bastará. Ex: 'lab04.py'
#
# Substitua também o número 1 pelo número do seu exercício,
# ou seja, se estiver programando o laboratório 5, substitua 1 por 5.
#
# PS: Se quiser realizar um teste em específico, por exemplo, para realizar o teste 4 no exercício 5, use:
#     teste_unico('C:/Users/aluno/Desktop/meuprograma.py', 5, 4)

from os import chdir, path
chdir(path.normpath(path.dirname(__file__)))

from susy import testar_tudo, teste_unico
testar_tudo('C:/Users/aluno/Desktop/meuprograma.py', 1)

"""Módulo para automatizar os testes de código da plataforma Susy"""

import ssl
import urllib.request
from subprocess import call
from tempfile import TemporaryFile
ssl._create_default_https_context = ssl._create_unverified_context


def _gethtml(url):
    """Acessa a url e retorna seu HTLM

    Args:
        url (str): url a ser acessada

    Returns:
        str: HTML do site
    """
    response = urllib.request.urlopen(url)
    bytestring = response.read()
    string = bytestring.decode('utf-8')
    return string


def _formatnum(num):
    """Formata números para terem 2 casas. Ex: 1 -> 01

    Args:
        n (int): Número a ser formatado

    Returns:
        str: Número formatado
    """
    num = '0'+str(num)
    num = f'{num[::-1]:.2}'
    return num[::-1]


def _gettest(exercise_num, test_num, file_type):
    """Faz download dos testes abertos do suzy

    Args:
        exercise_num (int): Numero do exercício. Ex: 1
        test_num (int): Numero do teste a ser baixado. Ex: 3
        file_type (str): Tipo do arquivo. 'in' ou 'out'

    Raises:
        ValueError: Caso test_num < 1, test_num > 10 ou exercício não liberado

    Returns:
        str: HTMl do teste
    """
    susyurl = 'https://susy.ic.unicamp.br:9999/mc102'
    exercises_page = _gethtml(susyurl)
    exercises_page = exercises_page.splitlines()
    lines_num = len(exercises_page)
    line_info = [line.find('HREF="../../mc102/') for line in exercises_page]
    exercises_avalible = lines_num - line_info.count(-1)

    if test_num-1 in range(10) and exercise_num-1 in range(exercises_avalible):
        test_num = _formatnum(test_num)
        exercise_num = _formatnum(exercise_num)
        fileurl = susyurl + f'/{exercise_num}/dados/arq{test_num}.{file_type}'
        return _gethtml(fileurl)
    else:
        raise ValueError(
            'Esse exercício, ou esse teste não estão disponíveis no susy')


def _tree(parent, child):
    """Formata duas strings de modo que se assemelhem a uma arvore

    Args:
        parent (str): String superior
        child (str): String inferior

    Returns:
        str: Arvore das duas strings
    """
    string = parent
    for line in child.splitlines():
        string += f'\n    | {line}'
    return string


def _exec_code(path, exercise_num, test_num):
    """Executa um código python com os valores do susy

    Args:
        path (str): Caminho para o arquivo. Ex: 'mc102/lab04'
        exercise_num (int): Número do exercício. Ex: 2
        test_num (int): Número do teste. Ex: 4

    Returns:
        (str, str, str): Tupla contendo, em ordem, o output do programa, o output esperado pelo susy, os erros levantados durante execução
    """
    susy_input = _gettest(exercise_num, test_num, 'in')
    susy_output = _gettest(exercise_num, test_num, 'out')
    with (
        TemporaryFile('w+') as stdin_file,
        TemporaryFile('w+') as stdout_file,
        TemporaryFile('w+') as stderr_file
    ):
        stdin_file.write(susy_input)
        stdin_file.seek(0)
        cmd = ['python3', path]
        call(cmd, stdin=stdin_file, stdout=stdout_file, stderr=stderr_file)
        stdout_file.seek(0)
        stderr_file.seek(0)
        return (stdout_file.read(), susy_output, stderr_file.read())


def _get_sheet(obtained, expected):
    """Formata os outputs obtidos e esperado em uma tabela, e compara se estão corretos

    Args:
        obtained (str): Output obtido
        expected (str): Output esperado

    Returns:
        str: Tabela
    """
    tabela = ''
    obtained = obtained.splitlines()
    expected = expected.splitlines()
    len_obtido = len(obtained)
    len_esperado = len(expected)
    len_max = max(len_esperado, len_obtido)
    linhas_obtidas = []
    linhas_esperadas = []
    for index in range(len_max):
        try:
            linhas_obtidas.append(obtained[index])
        except IndexError:
            linhas_obtidas.append('N/D')
        try:
            linhas_esperadas.append(expected[index])
        except IndexError:
            linhas_esperadas.append('N/D')
    maior_obtido = max([len(linha) for linha in linhas_obtidas]+[6]) + 2
    maior_esperado = max([len(linha) for linha in linhas_esperadas]+[8]) + 2
    str1 = "Obtido".center(maior_obtido)
    str2 = "Esperado".center(maior_esperado)
    tabela += f'{str1}|{str2}| Coincidem '
    for i, j in zip(linhas_obtidas, linhas_esperadas):
        if i == j:
            coincidem = '     ✅     '
        else:
            coincidem = '     ❌     '
        tabela += f'\n{i.center(maior_obtido)}|{j.center(maior_esperado)}|{coincidem}'
    return tabela


def teste_unico(path_arquivo, n_do_exercicio, n_do_teste):
    """Testa o programa indicado, com base em um teste do susy, e imprime o feedback da execução.

    Args:
        path_arquivo (str): Caminho para o arquivo. Ex: 'mc102/lab04.py'
        n_do_exercicio (_type_): Número do exercício. Ex: 1
        n_do_teste (_type_): Número do teste. Ex: 4
    """
    out_obtido, out_esperado, err = _exec_code(
        path_arquivo, n_do_exercicio, n_do_teste)
    titulo = f'Teste {_formatnum(n_do_teste)}:'
    if out_obtido == out_esperado:
        titulo += ' Certo!'
    else:
        titulo += ' Errado!'

    tabela = _get_sheet(out_obtido, out_esperado)
    if err == '':
        string = _tree(titulo, tabela)
        print(string + '\n')
    else:
        string = 'Os seguites erros foram encontrados durante a execução:'
        string = _tree(string, err)
        string = tabela + '\n\n' + string
        string = _tree(titulo, string)
        print(string + '\n')


def testar_tudo(path_arquivo, n_do_exercicio):
    """Testa o programa indicado, com base em um teste do susy, e imprime o feedback da execução.

    Args:
        path_arquivo (str): Caminho para o arquivo. Ex: 'mc102/lab04.py'
        n_do_exercicio (_type_): Número do exercício. Ex: 1
    """
    for n_do_teste in range(1, 11):
        teste_unico(path_arquivo, n_do_exercicio, n_do_teste)

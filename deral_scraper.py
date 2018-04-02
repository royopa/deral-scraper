# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from requests_html import HTMLSession


def get_dados_from_data(data_referencia, no_produto, tr_desc):
    data_referencia_formatada = data_referencia.strftime('%Y-%m-%d')
    url = 'http://celepar7.pr.gov.br/sima/cotdiat.asp?data='+data_referencia_formatada

    session = HTMLSession()
    response = session.get(url)
    
    if (response.status_code != 200):
        print(response.status_code)
        exit()

    return extract_data(response, data_referencia, no_produto, tr_desc)


def extract_data(response, data_referencia, no_produto, tr_desc):
    tabela = response.html.find('.mytable', first=True)
    try:
        vr_real = tabela.xpath(".//tr["+str(tr_desc+1)+"]/td[21]/font/text()")[0].strip()
    except IndexError:
        vr_real = None

    return {
        'dt_referencia': data_referencia,
        'no_produto': no_produto,
        'no_indicador': tabela.xpath(".//tr["+str(tr_desc)+"]/td[1]/font/text()")[0].strip().replace('  ',' '),
        'vr_real': vr_real
    }


def main():
    url = 'http://celepar7.pr.gov.br/sima/cotdiat.asp?data=2018-03-25'
    session = HTMLSession()
    response = session.get(url)
    
    if (response.status_code != 200):
        print(response.status_code)
        exit()

    tabela = response.html.find('.mytable', first=True)

    # algodão (descontinuada)
    no_produto = 'algodão'
    print(tabela.xpath(".//tr[2]/td[1]/font/text()")[0])
    print(tabela.xpath(".//tr[3]/td[21]/font/text()")[0])
    
    # arroz em casca sequeiro
    no_produto = 'arroz em casca'
    print(tabela.xpath(".//tr[5]/td[1]/font/text()")[0])
    print(tabela.xpath(".//tr[6]/td[21]/font/text()")[0])

    #Arroz Agulhinha em casca tipo 1 sc 60 Kg
    no_produto = 'arroz agulhinha'
    print(tabela.xpath(".//tr[8]/td[1]/font/text()")[0])
    print(tabela.xpath(".//tr[9]/td[21]/font/text()")[0])

    # Feijão Carioca tipo 1 sc 60 Kg
    no_produto = 'feijão carioca'
    print(tabela.xpath(".//tr[14]/td[1]/font/text()")[0])
    print(tabela.xpath(".//tr[15]/td[21]/font/text()")[0])

    # Feijão preto tipo 1 sc 60 Kg
    no_produto = 'feijão preto'
    print(tabela.xpath(".//tr[17]/td[1]/font/text()")[0])
    print(tabela.xpath(".//tr[18]/td[21]/font/text()")[0])

    # Milho amarelo tipo 1 sc 60 Kg
    no_produto = 'milho'
    print(tabela.xpath(".//tr[20]/td[1]/font/text()")[0])
    print(tabela.xpath(".//tr[21]/td[21]/font/text()")[0])

    # Soja industrial tipo 1 sc 60 Kg
    no_produto = 'soja'
    print(tabela.xpath(".//tr[23]/td[1]/font/text()")[0])
    print(tabela.xpath(".//tr[24]/td[21]/font/text()")[0])

    # Trigo pão PH 78 sc 60 Kg
    no_produto = 'trigo'
    print(tabela.xpath(".//tr[26]/td[1]/font/text()")[0])
    print(tabela.xpath(".//tr[27]/td[21]/font/text()")[0])

    # Boi em pé arroba
    no_produto = 'boi'
    print(tabela.xpath(".//tr[29]/td[1]/font/text()")[0])
    print(tabela.xpath(".//tr[30]/td[21]/font/text()")[0])

    # Pesquisa descontinuada (Frango vivo)
    no_produto = 'frango vivo'
    print(tabela.xpath(".//tr[32]/td[1]/font/text()")[0])
    print(tabela.xpath(".//tr[33]/td[21]/font/text()")[0])

    # Erva-mate folha em barranco arroba
    no_produto = 'erva-mate'
    print(tabela.xpath(".//tr[35]/td[1]/font/text()")[0])
    print(tabela.xpath(".//tr[36]/td[21]/font/text()")[0])

    # Suíno em pé tipo carne não integrado kg
    no_produto = 'suíno'
    print(tabela.xpath(".//tr[38]/td[1]/font/text()")[0])
    print(tabela.xpath(".//tr[39]/td[21]/font/text()")[0])

    # Vaca em pé (padrão corte) arroba
    no_produto = 'vaca'
    print(tabela.xpath(".//tr[41]/td[1]/font/text()")[0])
    print(tabela.xpath(".//tr[42]/td[21]/font/text()")[0])

    # Café beneficiado bebida dura - tipo 6 sc 60 Kg
    no_produto = 'café beneficiado'
    print(tabela.xpath(".//tr[44]/td[1]/font/text()")[0])
    print(tabela.xpath(".//tr[45]/td[21]/font/text()")[0])

    # Mandioca padrão de amido 580 g tonelada
    #mandioca
    no_produto = 'mandioca'
    print(tabela.xpath(".//tr[47]/td[1]/font/text()")[0])
    print(tabela.xpath(".//tr[48]/td[21]/font/text()")[0])

'''
Data
CAFÉ
FEIJÃO DE COR
FEIJÃO PRETO
MILHO COMUM
SOJA INDUSTRIAL
TRIGO
BOI
FRANGO
SUINO EM PÉ
'''

def indicadores_deral():
    dados = [
        {'id': 16, "no_indicador":"Pesquisa descontinuada (Arroz em casca sequeiro)"},
        {'id': 1617, "no_indicador":"Arroz Agulhinha em casca tipo 1 sc 60 Kg"},
        {'id': 1618, "no_indicador":"Feijão Carioca tipo 1 sc 60 Kg"},
        {'id': 1619, "no_indicador":"Feijão preto tipo 1 sc 60 Kg"},
        {'id': 1620, "no_indicador":"Milho amarelo tipo 1 sc 60 Kg"},
        {'id': 1621, "no_indicador":"Soja industrial tipo 1 sc 60 Kg"},
        {'id': 1622, "no_indicador":"Trigo pão PH 78 sc 60 Kg"},
        {'id': 1623, "no_indicador":"Boi em pé arroba"},
        {'id': 1624, "no_indicador":"Pesquisa descontinuada (Frango vivo)"},
        {'id': 1625, "no_indicador":"Erva-mate folha em barranco arroba"},
        {'id': 1626, "no_indicador":"Suíno em pé tipo carne não integrado kg"},
        {'id': 1627, "no_indicador":"Vaca em pé (padrão corte) arroba"},
        {'id': 1628, "no_indicador":"Café beneficiado bebida dura - tipo 6 sc 60 Kg"},
        {'id': 1629, "no_indicador":"Mandioca padrão de amido 580 g tonelada"},
        {'id': 1630, "no_indicador":"Pesquisa descontinuada (Algodão)"}
    ]
    return dados


def get_id_indicador(no_indicador):
    dados = indicadores_deral()
    for dado in dados:
        if dado['no_indicador'] == no_indicador:
            return dado['id']


def get_dados():
    dados = [
        { 'no_produto': 'algodão', 'tr_desc': 2},
        { 'no_produto': 'arroz em casca', 'tr_desc': 5},
        { 'no_produto': 'arroz agulhinha', 'tr_desc': 8},
        { 'no_produto': 'feijão carioca', 'tr_desc': 14},
        { 'no_produto': 'feijão preto', 'tr_desc': 17},
        { 'no_produto': 'milho', 'tr_desc': 20},
        { 'no_produto': 'soja', 'tr_desc': 23},
        { 'no_produto': 'trigo', 'tr_desc': 26},
        { 'no_produto': 'boi', 'tr_desc': 29},
        { 'no_produto': 'frango vivo', 'tr_desc': 32},
        { 'no_produto': 'erva-mate', 'tr_desc': 35},
        { 'no_produto': 'suíno', 'tr_desc': 38},
        { 'no_produto': 'vaca', 'tr_desc': 41},
        { 'no_produto': 'café beneficiado', 'tr_desc': 44},
        { 'no_produto': 'mandioca', 'tr_desc': 47}
    ]
    
    return dados

if __name__ == '__main__':
    main()
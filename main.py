# -*- coding: utf-8 -*-
import csv
import os
import datetime
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
        'vr_real': float(vr_real)
    }


def main():
    data_referencia = datetime.date.today()
    #start_date = datetime.date(2018, 3, 27)
    start_date = data_referencia
    end_date = data_referencia + datetime.timedelta(1)
    dates_2010_2018 = [ start_date + datetime.timedelta(n) for n in range(int ((end_date - start_date).days))]

    base_file_name = 'precos_deral_base.csv'
    path_file_base = os.path.join('bases', base_file_name)

    for data_referencia in dates_2010_2018:
        print(data_referencia)
        if (data_referencia.weekday() > 4):
            continue

        for index, dado in enumerate(get_dados()):
            dados_site = get_dados_from_data(data_referencia, dado['no_produto'], dado['tr_desc'])

            if dados_site['vr_real'] is '':
                print('dados não disponíveis', dado['no_produto'])
                continue

            if dados_site['vr_real'] is None:
                print('dados não disponíveis', dado['no_produto'])
                continue

            # faz o append no csv da base
            with open(path_file_base, 'a', newline='') as baseFile:
                fieldnames = ['dt_referencia', 'no_produto', 'no_indicador', 'vr_real']
                writer = csv.DictWriter(baseFile, fieldnames=fieldnames, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
                row_inserted = dados_site
                writer.writerow(row_inserted)
                print('Dado inserido no arquivo base:', path_file_base, row_inserted)

    print('Registros deral importados com sucesso')
    return True


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
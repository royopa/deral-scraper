# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from requests_html import HTMLSession
import parser
import requests
from tqdm import tqdm
import os
import csv
import time


def download_file(url, file_name):
    response = requests.get(url, stream=True)
    with open(file_name, "wb") as handle:
        for data in tqdm(response.iter_content()):
            handle.write(data)
    handle.close()


def get_link_codigos(paginas = []):
    url = 'http://www.agricultura.pr.gov.br/modules/qas/categoria.php'
    session = HTMLSession()
    links = []

    for page in paginas:
        print('pagina:', page)

        params = {
            'cod_categoria': '28',
            'pagina': str(page),
            'ordenacao': 'data',
            'tipo_ordem': 'DESC',
            'filtroTitulo': '',
            'filtroDataIni': '1425401400',
            'filtroDataFim': '1865401400'
        }
        
        time.sleep(.2)
        response = session.get(url, params=params)

        if (response.status_code != 200):
            print('erro no acesso a página: ', url, params)
            continue
        try:
            table = response.html.find('#content > div.blockContent > table', first=True)
        except Exception as e:
            print('error', e)
            continue
        
        try:
            links_page = table.links
            links.append(links_page)
        except parser.ParserError:
            print('erro')
            continue

    codigos = []
    print(links)
    for link in links:
        for l in link:
            if (l.startswith('aviso.php?codigo=')):
                codigo = l[-4:]
                # faz o append no csv da base
                with open('codigos.csv', 'a', newline='') as baseFile:
                    fieldnames = ['codigo']
                    writer = csv.DictWriter(baseFile, fieldnames=fieldnames, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
                    row_inserted = { 'codigo': codigo }
                    writer.writerow(row_inserted)
                print(codigo)                
                codigos.append(codigo)
    
    print(codigos)
    return codigos            


def get_link_planilhas(codigos = []):
    # agora que já tem os códigos, vai para a página para baixar o xls correspondente
    url = 'http://www.agricultura.pr.gov.br/modules/qas/aviso.php'
    planilhas = []
    session = HTMLSession()
   
    for codigo in codigos:
        print('código:', codigo)
        params = { 'codigo': str(codigo) }
        time.sleep(.1)
        response = session.get(url, params=params)

        if (response.status_code != 200):
            continue

        try:
            links_page = response.html.links
        except Exception as e:
            links_page = []
            print('erro', e)
            continue

        for link in links_page:
            if (link.endswith('_impressao.xls')):
                # faz o append no csv da base
                with open('urls.csv', 'a', newline='') as baseFile:
                    fieldnames = ['url']
                    writer = csv.DictWriter(baseFile, fieldnames=fieldnames, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
                    row_inserted = { 'url': 'http://www.agricultura.pr.gov.br/modules/qas/'+link }
                    writer.writerow(row_inserted)
                planilhas.append(link)
                download_planilhas([link])
    
    return planilhas


def download_planilhas(planilhas = []):
    url = 'http://www.agricultura.pr.gov.br/modules/qas/'

    for planilha in planilhas:
        url_planilha = url+planilha
        print(url_planilha)
        name_file = url_planilha.split('/')[-1]
        path_file = os.path.join('downloads', name_file)
        if os.path.exists(path_file):
            continue
        download_file(url_planilha, path_file)


def main():
    #paginas = list(range(1, 2, 1))
    paginas = list(range(1, 26, 1))
    print(paginas)
    codigos = get_link_codigos(paginas)
    print(codigos)

    # agora que já tem os códigos, vai para a página para baixar o xls correspondente
    planilhas = []
    if len(codigos) > 0:
        print(len(codigos))
        time.sleep(10)
        planilhas = get_link_planilhas(codigos)
    
    print(planilhas)
    if len(planilhas) > 0:
        print(len(planilhas))
        time.sleep(.3)
        #download_planilhas(planilhas)


if __name__ == '__main__':
    main()
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
            'filtroDataIni': '1425401400'
        }
        
        response = session.get(url, params=params)
        time.sleep(2)

        if (response.status_code != 200):
            print('erro no acesso a página: ', url, params)
            continue
        
            print(response.html)

        try:
            table = response.html.find('#content > div.blockContent > table', first=True)
        except Exception as e:
            print('', e)
            continue
        
        try:
            links_page = table.links
            links.append(links_page)
        except parser.ParserError:
            print('erro')
            continue

    codigos = []
    for link in links:
        for l in link:
            if (l.startswith('aviso.php?codigo=')):
                codigo = l[-4:]
                codigos.append(codigo)
    
    return codigos            


def get_link_planilhas(codigos = []):
    # agora que já tem os códigos, vai para a página para baixar o xls correspondente
    url = 'http://www.agricultura.pr.gov.br/modules/qas/aviso.php'
    planilhas = []
    session = HTMLSession()
   
    for codigo in codigos:
        print('código:', codigo)
        params = { 'codigo': str(codigo) }
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
                    row_inserted = { 'url': link }
                    writer.writerow(row_inserted)
                planilhas.append(link)
    
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
    
    # agora que já tem os códigos, vai para a página para baixar o xls correspondente
    if len(codigos) > 0:
        print(len(codigos))
        planilhas = get_link_planilhas(codigos)
    

    if len(planilhas) > 0:
        print(len(planilhas))
        download_planilhas(planilhas)


if __name__ == '__main__':
    main()
# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from requests_html import HTMLSession
import parser
import requests
from tqdm import tqdm
import os


def download_file(url, file_name):
    response = requests.get(url, stream=True)
    with open(file_name, "wb") as handle:
        for data in tqdm(response.iter_content()):
            handle.write(data)
    handle.close()


def main():
    url = 'http://www.agricultura.pr.gov.br/modules/qas/categoria.php'
    session = HTMLSession()
    links = []
    
    #for page in range(1, 2, 1):
    for page in range(1, 26, 1):
        print('pagina:', page)
        params = {
            'cod_categoria': str(28),
            'pagina': str(page)
        }
        response = session.get(url, params=params)
        
        if (response.status_code != 200):
            continue
        
        try:
            table = response.html.find('#content > div.blockContent > table', first=True)
        except parser.ParserError:
            print('erro')
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

    # agora que já tem os códigos, vai para a página para baixar o xls correspondente
    url = 'http://www.agricultura.pr.gov.br/modules/qas/aviso.php'
    planilhas = []
    
    for codigo in codigos:
        print('código:', codigo)

        params = {
            'codigo': str(codigo)
        }

        response = session.get(url, params=params)

        if (response.status_code != 200):
            continue        

        try:
            links_page = response.html.links
        except KeyError:
            links_page = []
            print('erro')
            continue

        for link in links_page:
            if (link.endswith('_impressao.xls')):
                planilhas.append(link)


    url = 'http://www.agricultura.pr.gov.br/modules/qas/'
    
    for planilha in planilhas:
        url_planilha = url+planilha
        print(url_planilha)
        name_file = url_planilha.split('/')[-1]
        path_file = os.path.join('downloads', name_file)
        if not os.path.exists(path_file):
            download_file(url_planilha, path_file)


if __name__ == '__main__':
    main()
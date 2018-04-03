# -*- coding: utf-8 -*-
import csv
from requests_html import HTMLSession
import time
import os


def list_files(dir_files):
    if not os.path.exists(dir_files):
        os.makedirs(dir_files)

    return filter(
        lambda x: not os.path.isdir(os.path.join(dir_files, x)),
        os.listdir(dir_files)
    )


def get_link_planilhas(codigos, ultimo_codigo):
    # agora que já tem os códigos, vai para a página para baixar o xls correspondente
    url = 'http://www.agricultura.pr.gov.br/modules/qas/aviso.php'
    planilhas = []
    session = HTMLSession()
   
    for codigo in codigos:
        if int(codigo) < ultimo_codigo:
            continue

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
            get_link_planilhas([codigo], int(codigo))
            continue

        for link in links_page:
            if (link.endswith('_impressao.xls')):
                # faz o append no csv da base
                with open('urls.csv', 'a', newline='') as baseFile:
                    fieldnames = ['url']
                    writer = csv.DictWriter(baseFile, fieldnames=fieldnames, delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
                    row_inserted = { 'url': 'http://www.agricultura.pr.gov.br/modules/qas/'+link }
                    writer.writerow(row_inserted)
                print(row_inserted)
                planilhas.append(link)
    return planilhas


def main():
    with open('codigos.csv', 'r') as f:
        reader = csv.reader(f)
        urls_list = list(reader)
    
    list_cleaned = []
    for url in urls_list:
        if url[0] not in list_cleaned:
            list_cleaned.append(url[0])
    
    codigo = 5469
    get_link_planilhas(sorted(list_cleaned), codigo)
    
    #for codigo in list_cleaned:
        #print(codigo)
    #print(len(list_cleaned))

    #dir_files = 'C:\c090762\projects\deral-scraper\downloads'
    #downloaded_files = list(list_files(dir_files))
    #print(downloaded_files)


if __name__ == '__main__':
    main()
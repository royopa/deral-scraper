# -*- coding: utf-8 -*-
import wget
import os
import csv


def main():
    with open('urls.csv', 'r') as f:
        reader = csv.reader(f)
        urls_list = list(reader)
    

    list_cleaned = []
    for url in urls_list:
        if url[0] not in list_cleaned:
            list_cleaned.append(url[0])
    
    for url in list_cleaned:
        name_file = url.split('/')[-1]
        print(name_file)
        path_file = os.path.join('downloads', name_file)

        if not os.path.exists(path_file):
            wget.download(url, path_file)


if __name__ == '__main__':
    main()
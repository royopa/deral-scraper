[![Build Status](https://travis-ci.org/royopa/deral-scraper.svg?branch=master)](https://travis-ci.org/royopa/deral-scraper)

# deral-scraper

Projeto para captura das cotações diária de preços DERAL - Departamento de Economia Rural - SIMA - Sistema de informação do mercado agrícola do Governo do Estado do Paraná  

## Instalando

```
> pip install --user pipenv
> pipenv shell
> python main.py
```

## Links
http://www.agricultura.pr.gov.br/modules/qas/categoria.php?cod_categoria=28

http://celepar7.pr.gov.br/sima/cotdiat.asp?data=2010-01-04

http://www.agricultura.pr.gov.br/modules/qas/categoria.php?pagina=25&cod_categoria=28&ordenacao=data&tipo_ordem=DESC&filtroTitulo=&filtroDataIni=1425401400&filtroDataFim=1522682400

## Download das planilhas

Visto que a página trava para se tentar pegar os links dos arquivos xls, foi necessário criar
um arquivo intermediário [urls.csv](urls.csv) contendo os links das planilhas para serem baixadas
em processo posterior.
import math

from bs4 import BeautifulSoup
import requests
import re
import math
import pandas as pd
import shutil
entrada = ""
url = "https://www.olx.com.br/estado-mg/regiao-de-montes-claros-e-diamantina?q=guitarra&o=1"

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
    Chrome/111.0.0.0 Safari/537.36'}

site = requests.get(url,headers=headers)
soup = BeautifulSoup(site.content, 'html.parser')

qtd_itens=soup.find('p',class_='sc-hGPBjI jJgSKc').get_text().strip()
if 'de ' in qtd_itens:
    inicio = qtd_itens.find('de ')
    fim = qtd_itens.find('resultados', inicio)
    qtd_itens = qtd_itens[inicio+2:fim]

print(qtd_itens)
ultima_pagina = math.ceil(int(qtd_itens.replace('.',''))/50)
print(ultima_pagina)

series_produtos = {'nome': [], 'preco': [], 'link': []}

if ultima_pagina > 100:
    rangeMax = 100
else:
    rangeMax = ultima_pagina

for i in range (1,rangeMax):
    nome = ''
    preco = ''
    link = ''

    url = f'https://www.olx.com.br/estado-mg/regiao-de-montes-claros-e-diamantina?q=guitarra&o={i}'
    site = requests.get(url,headers=headers)
    soup = BeautifulSoup(site.content, 'html.parser')

    cards = soup.find_all('section', class_=re.compile('horizontal undefined'))
    #print(cards)

    for card in cards:
        try:
            nome = card.find('h2', class_=re.compile('horizontal title')).get_text().strip()
            preco = card.find('h3', class_=re.compile('horizontal price')).get_text().strip()
            link = card.find_all('a',href=True)
            for a in link:
                link = a['href']
        except :
            print('produto não encontrado')
        print('nome : ',nome)
        print('preco : ',preco)
        print(link)
        print('xxxxxxxxxxxxxxx')

        series_produtos['nome'].append(nome)
        series_produtos['preco'].append(preco)
        series_produtos['link'].append(link)
df = pd.DataFrame(series_produtos)
(df.to_excel('.\olxScrap.xlsx'))
df.to_csv('olxScrapp.csv')
#----------------IMPORTS--------------#
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from time import sleep
import pandas as pd
#--------------------------------------#
pesquisa = input("Digite o que você quer buscar: ")
#----------------OPTIONS---------------#
options = Options()
options.add_argument('--headless')
#options.add_argument('window-size=400,800')
#---------------NAVEGAÇÃO--------------#
url_dentalSpeed = "https://www.dentalspeed.com/"
navegador = webdriver.Edge(options=options)
navegador.get(url_dentalSpeed)
sleep(2)
#--------------------------------------#

elemento = navegador.find_element(By.ID, "search")
elemento.send_keys(pesquisa)
elemento.submit()
sleep(4)

page_content = navegador.page_source

site = BeautifulSoup(page_content, 'html.parser')
lista_de_materiais = site.find('ol', attrs={'class': 'products list items product-items'})
materiais = lista_de_materiais.findAll('li', attrs={'class': 'item product-item'})

listaProdutos = []
for material in materiais:
    produto = material.find('span', attrs={'data-bind': 'text: $parent.cardJs.decodeStr($data.name)'})
    marca = material.find('span', attrs={'data-bind': 'text: $data.details.brand'})
    preco = material.find('span', attrs={'data-bind': "attr: {'data-price-amount' : $data.price}"})['data-price-amount']
    listaProdutos.append([produto.text, marca.text, float(preco)])

dados = pd.DataFrame(listaProdutos, columns=['Produto', 'Marca', 'Preço'])
arquivo_excel = pesquisa + '.xlsx'
dados.to_excel(arquivo_excel, index=False)
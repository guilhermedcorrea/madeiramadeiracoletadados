import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import visibility_of_element_located
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import lxml.html as parser
import requests
import csv
import time
import re
import json
from selenium.webdriver.common.keys import Keys
from datetime import datetime


driver = webdriver.Chrome(ChromeDriverManager().install())


def scroll():
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
        lastCount = lenOfPage
        time.sleep(3)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True


def informa_marca():
    url = "https://www.madeiramadeira.com.br/"

    driver.get(url)
    time.sleep(1)

    brand = driver.find_element_by_css_selector("#searchAutoComplete")
    brand.send_keys("Deca")

    busca = driver.find_element_by_css_selector("#__next > div > nav > div > div.cav--c-fEpGcZ > div > form > button > i > svg").click()

def paginas():
    scroll()
    lista_paginas = []
    num_pages = driver.find_elements_by_xpath('//*[@id="__next"]/div/main/div[4]/div/div/div/div[2]/div/div[2]/div/div/div[1]/div/ul/li/a/span')
    for num in num_pages:
        lista_paginas.append(num.text)

    page = lista_paginas[-1]
    page = int(page)
    return page

def urls_produtos():
    lista_urls = []
    qtd_paginina = paginas()
    for i in range(1,qtd_paginina):
        pagina =  f'https://www.madeiramadeira.com.br/busca?q=Deca&page={i}'
        try:
            driver.get(pagina)
        except:
            pass
        
        time.sleep(1)
        scroll()
        try:
            urlsprodutos = driver.find_elements_by_xpath('//*[@id="__next"]/div/main/div[4]/div/div/div/div[2]/div/div[1]/div/div/article/a')
            for urlsp in urlsprodutos:
                print(urlsp.get_attribute("href"))
                lista_urls.append(urlsp.get_attribute("href"))
        except:
            pass
    return lista_urls

def get_produtos():
    lista_dicts = []
    urls = urls_produtos()
    for url in urls:
        try:
            driver.get(url)
        except:
            pass
        time.sleep(1)
        driver.implicitly_wait(10)
        try:
            jsons = driver.find_elements_by_css_selector("head > script:nth-child(51)")[0].get_attribute('textContent')
            dicts = json.loads(jsons)
            lista_dicts.append(dicts)
        except:
            print("Erro jsons")
        
        #rola pagina até campo cep
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight-400);")

        #Informa cep
        try:
            input_cep = driver.find_element_by_css_selector('#Insira\ o\ CEP')
            input_cep.send_keys('13013000')
            calcular = driver.find_element_by_css_selector('#__next > div > main > div:nth-child(2) > div.cav--c-gkGAKm.cav--c-gkGAKm-ihkScrX-css > div:nth-child(2) > div > div.cav--c-lesPJm.cav--c-lesPJm-ifGHEql-css > div.cav--c-lesPJm.cav--c-cmpvrW.cav--c-cmpvrW-hewRfn-border-bordered > div > div:nth-child(2) > button').click()
        except:
            pass
        
        time.sleep(3)
        try:
            nome_produto = driver.find_elements_by_xpath('//*[@id="__next"]/div/main/div[2]/div[2]/div[2]/div/div[2]/h1')[0].text
            print()
            print('PRODUTO URL ~~ > ',url)
            print(nome_produto)
            print()
        except:
            pass
        prazos = driver.find_elements_by_xpath('//*[@id="__next"]/div/main/div[2]/div[2]/div[2]/div/div[2]')
        for prazo in prazos:
            sep = prazo.text.split("\n")
            for i, num in enumerate(sep):
                if re.search('Frete e prazo', num):
                   valores_frete = sep[i:]
                   print(valores_frete)
                   print()

        print(dicts)


informa_marca()
get_produtos()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import requests,re
from bs4 import BeautifulSoup
from lxml import html,etree
import pandas as pd



class Scraping_Startup(object):
    def __init__(self, serches):
        self.serach = searchs

    def getCardsURL(self):
        driver = webdriver.Chrome()

        urls = []
        for ss in self.searchs:
            url = 'https://startupbase.abstartups.com.br/startups?query=%s&hitsPerPage=80&page=1' %(ss)


            driver.get(url)
            time.sleep(2)

            restaurant_information = driver.find_elements_by_xpath('//*[@class="sb-card sb-card__card_size_full"]')
            restaurant_link = driver.find_element_by_xpath('//a')
            pages = driver.find_elements_by_xpath('//*[@class="pagination-page page-item"]')


            for p in range(0,int(len(pages) / 2)):
                 url2 = 'https://startupbase.abstartups.com.br/startups?query=%s&hitsPerPage=80&page=%d' %(ss,p+1)
                 driver.get(url2)
                 restaurant_information = driver.find_elements_by_xpath('//*[@class="sb-card sb-card__card_size_full"]')
                 for i in restaurant_information:
                     urls.append(i.get_attribute("href"))

        self.urls = list(dict.fromkeys(urls))

    def createdictionayLAteral(self):
        splits = ['Últ Atualização',
         'Tipo de Organização',
         'Fundação',
         'Status',
         'Tamanho do time',
         'Mercado',
         'Público-alvo',
         'Modelo de Receita',
         'Momento',
         'Endereço']


        argumenSplits = ['None','None','None','None','None','None','None','None','None','None']



        self.splicsdict = dict(zip(splits, argumenSplits))

        return (self.splicsdict)


    def padraoLat(self, splicsdict,d):
        for i in splicsdict.keys():
            if i not in d:
                d.update({i:splicsdict[i]})
        return (d)


    def getInformations(self):

        self.information = []
        for u in self.urls:
            driver.get(u)
            time.sleep(2)

            local = 'None'
            description = 'None'
            name = 'None'
            rest_local = driver.find_elements_by_xpath('//*[@class="page__location text-center text-sm-left"]')[0].text.split('\n')
            rest_nome = driver.find_elements_by_xpath('//*[@class="mt-4 mt-sm-0"]')[0].text.split('\n')
            rest_descr = driver.find_elements_by_xpath('//*[@class="page__short-description font-weight-light font-italic text-center text-sm-left wordwrap"]')[0].text.split('\n')
            if len(rest_local) > 0:
                local = rest_local[0]
            if len(rest_nome) > 0:
                name = rest_nome[0]
            if len(rest_descr) > 0:
                description = rest_descr[0]

            infoLat = driver.find_element_by_xpath('//*[@class="text-center"]')
            par = infoLat.text.split('\n')
            argu = []
            for i in range(len(par)):
                if par[i] == 'Endereço':
                    argu.append((par[i],par[(i+1):]))
                elif par[i] in splits:
                    argu.append((par[i],par[(i+1)]))

            d = {}
            for a, b in argu:
                d[a]= b

            argud = self.padraoLat(self.splicsdict(), d)


            data = argud
            data['A startUp Name'] = name
            data['descrição'] = description
            data['Localidade'] = local

            sobr = driver.find_elements_by_xpath('//*[@class="pb-4 wordwrap"]')[0].text.split('\n')

            team = driver.find_elements_by_xpath('//*[@class="page__section"]')[0].text.split('\n')

            data['Time Fundador'] = team[1:]

            data['Sobre'] = sobr


            self.information.append(data)

        self.dataFrame = pd.DataFrame.from_dict(self.information)

    def writeXLS(self, directoryy, filename):

        writer = pd.ExcelWriter(directory + filename)
        self.dataFrame.to_excel(writer, 'Sheet 1', index=False)
        writer.save()




if __name__ == '__main__':

    searchs = ['food', 'foodtech', 'foodservice', 'food-service', 'restaurant','restaurante',
                'restaurantes', 'hospitalidade', 'bar', 'bares', 'comida', 'alimentação', 'alimentação-fora-do-lar']


    scrap = Scraping_Startup(serches=serches)

    scrap.getCardsURL()

    scrap.getInformations()

    scrap.writeXLS(directory='dir', filename='TestScrap.xls')

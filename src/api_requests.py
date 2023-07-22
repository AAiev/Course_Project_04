import requests
import json
from abc import ABC, abstractmethod
import urllib.parse
import os
from pprint import pprint

SUPERJOB_API_KEY = 'v3.r.137693076.8c0a621f62c1bc4c0fadc3056207d620545fa9c6.3a2d874af9ab61cef98ab134333dd3f98ecc486c'

# API_URL = 'https://api.hh.ru/'

class RequestsAPI(ABC):
    abstractmethod
    def __init__(self, keyword=''):
        self.keyword = keyword

    @abstractmethod
    def get_vacancies(self, keyword=''):
        pass

    @abstractmethod
    def print_info(self):
        pass




class HeadHunterAPI(RequestsAPI):
    def __init__(self, keyword):
        self.keyword = 'NAME:' + keyword
        # self.data_req = {}

    def get_vacancies(self):
        params = {'text': self.keyword}
        req = requests.get('https://api.hh.ru/vacancies', params) # Посылаем запрос к API
        data_req = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
        req.close()
        jsObj = json.loads(data_req)
        return jsObj

    def print_info(self):
        for i in self.get_vacancies()['items']:
            print(i)


class SuperjobAPI(RequestsAPI):
    headers = {'X-Api-App-Id': SUPERJOB_API_KEY}
    def __init__(self, keyword):
        headers = {'X-Api-App-Id': SUPERJOB_API_KEY}
        self.keyword = keyword
        # self.data_req = {}

    def get_vacancies(self):
        req = requests.get('https://api.superjob.ru/2.0/vacancies/?' + 'srws=10&' + 'keys=' + self.keyword, headers=self.headers)
        data_req = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
        req.close()
        jsObj = json.loads(data_req)
        return jsObj

    def print_info(self):
        for i in self.get_vacancies()['objects']:
            print(i)

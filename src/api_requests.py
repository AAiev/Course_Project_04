import requests
import json
from abc import ABC, abstractmethod

SUPERJOB_API_KEY = 'v3.r.137693076.8c0a621f62c1bc4c0fadc3056207d620545fa9c6.3a2d874af9ab61cef98ab134333dd3f98ecc486c'


class RequestsAPI(ABC):
    @abstractmethod
    def __init__(self, keyword=''):
        self.keyword = keyword

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def print_info(self):
        pass


class HeadHunterAPI(RequestsAPI):
    def __init__(self, keyword):
        self.keyword = 'NAME:' + keyword
        # self.data_req = {}

    def get_vacancies(self, keyword=''):
        """Выдает вакансии по ключевому слову keyword"""
        params = {'text': self.keyword}
        req = requests.get('https://api.hh.ru/vacancies', params)  # Посылаем запрос к API
        data_req = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
        req.close()
        json_oobj = json.loads(data_req)
        return json_oobj

    def print_info(self):
        """develop-метод, для отображения инфы по запросу"""
        for i in self.get_vacancies()['items']:
            print(i)


class SuperjobAPI(RequestsAPI):
    headers = {'X-Api-App-Id': SUPERJOB_API_KEY}

    def __init__(self, keyword):
        self.keyword = keyword

    def get_vacancies(self, keyword=''):
        """Выдает вакансии по ключевому слову keyword"""
        req = requests.get('https://api.superjob.ru/2.0/vacancies/?' + 'srws=10&' + 'keys=' + self.keyword,
                           headers=self.headers)
        data_req = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
        req.close()
        json_oobj = json.loads(data_req)
        return json_oobj

    def print_info(self):
        """develop-метод, для отображения инфы по запросу"""
        for i in self.get_vacancies()['objects']:
            print(i)

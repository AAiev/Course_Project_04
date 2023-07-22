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

    def edit_list_get_vacancies(self):
        correct_list_vacancies = []
        for i in self.get_vacancies()['items']:
            vacancy_info = {}
            vacancy_info['id'] = f"id: {i['id']}"
            vacancy_info['employer'] = f"Компания: {i['employer']['name']}"
            vacancy_info['profession'] = f" Должность: {i['name']}"
            if i['salary'] == None:
                vacancy_info['salary'] = 'Зарплата не указана'
            elif i['salary']['from'] == None:
                vacancy_info['salary'] = f"Зарплата: до {i['salary']['to']} {i['salary']['currency']}"
            elif i['salary']['to'] == None:
                vacancy_info['salary'] = f"Зарплата: от {i['salary']['from']} {i['salary']['currency']}"
            else:
                vacancy_info['salary'] = f"Зарплата: {i['salary']['from']}-{i['salary']['to']} {i['salary']['currency']}"
            vacancy_info['town'] = f"Город: {i['area']['name']}"
            vacancy_info['requirement'] = f"Требования: {i['snippet']['requirement']}"
            vacancy_info['experience'] = f"Требуемый опыт: {i['experience']['name']}"
            vacancy_info['employment'] = f"Занятость: {i['employment']['name']}"
            vacancy_info['url'] = f"Ссылка на вакансию: https://www.hh.ru/vacancy/{vacancy_info['id'][4:]}"
            vacancy_info['employment'] = f"Занятость: {i['employment']['name']}"

            correct_list_vacancies.append(vacancy_info)
        return correct_list_vacancies


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

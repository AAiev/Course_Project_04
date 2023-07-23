import requests
import json
from abc import ABC, abstractmethod


class RequestsAPI(ABC):

    @abstractmethod
    def get_request(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_vacancies(self, *args, **kwargs):
        pass


class ParsingError(Exception):
    """Общий класс исключения для скриптов"""

    def __init__(self, *args):
        self.message = args[0] if args else 'Ошибка получения вакансий.'

    def __str__(self):
        return self.message


class ParentAPI(RequestsAPI):
    def __init__(self):
        self.keyword = ''
        self.url = ''
        self.param = []
        self.headers = None
        self.key_with_vacancies = ''

    def get_request(self):
        req = requests.get(self.url, self.params)
        if req.status_code != 200:
            raise ParsingError(f'Ошибка получения вакансий. Код статуса: {req.status_code}')
        else:
            return req

    def get_vacancies(self, req):
        """Выдает вакансии по ключевому слову keyword"""
        data_req = req.content.decode()  # Декодируем его ответ, чтобы Кириллица отображалась корректно
        json_obj = json.loads(data_req)
        return json_obj

    def print_info(self, vacancy_list):
        """develop-метод, для отображения инфы по запросу"""
        if self.key_with_vacancies in vacancy_list:
            for i in vacancy_list[self.key_with_vacancies]:
                print(i)
        else:
            for i in vacancy_list:
                print(i)


class HeadHunterAPI(ParentAPI):
    def __init__(self, keyword):
        super().__init__()
        self.keyword = keyword
        self.params = {'text': self.keyword,
                       "per_page": 10,
                       "page": 0,
                       }
        self.url = 'https://api.hh.ru/vacancies'
        self.key_with_vacancies = 'items'

    def edit_list_get_vacancies(self, vacancy_list):
        correct_list_vacancies = []
        for i in vacancy_list[self.key_with_vacancies]:
            vacancy_info = {'id': i['id'],
                            'company': i['employer']['name'],
                            'profession': i['name'],
                            'salary_currency': i['salary']['currency'],
                            'town': i['area']['name'],
                            'requirement': i['snippet']['requirement'],
                            'experience': i['experience']['name'],
                            'employment': i['employment']['name']
                            }
            if i['salary'] is None:
                vacancy_info['salary_from'] = None
                vacancy_info['salary_to'] = None
            else:
                vacancy_info['salary_from'] = i['salary']['from']
                vacancy_info['salary_to'] = i['salary']['to']
            vacancy_info['url'] = f"https://www.hh.ru/vacancy/{vacancy_info['id'][4:]}"
            correct_list_vacancies.append(vacancy_info)
        return correct_list_vacancies


class SuperjobAPI(ParentAPI):

    def __init__(self, keyword):
        super().__init__()
        self.keyword = keyword
        self.params = {'count': 10,
                       'keyword': self.keyword}
        self.headers = {'X-Api-App-Id':
                        'v3.r.137693076.8c0a621f62c1bc4c0fadc3056207d620545fa9c6.'
                        '3a2d874af9ab61cef98ab134333dd3f98ecc486c'}
        self.url = 'https://api.superjob.ru/2.0/vacancies'
        self.key_with_vacancies = 'objects'

    def get_request(self):
        req = requests.get(self.url, self.params, headers=self.headers)
        if req.status_code != 200:
            raise ParsingError(f'Ошибка получения вакансий. Код статуса: {req.status_code}')
        else:
            return req

    def edit_list_get_vacancies(self, vacancy_list):
        correct_list_vacancies = []
        for i in vacancy_list[self.key_with_vacancies]:
            vacancy_info = {'id': i['id'],
                            'company': i['firm_name'],
                            'profession': i['profession'],
                            'salary_from': i['payment_from'],
                            'salary_to': i['payment_to'],
                            'salary_currency': i['currency'],
                            'town': i['town']['title'],
                            'requirement': i['candidat'],
                            'experience': i['experience']['title'],
                            'employment': i['type_of_work']['title'],
                            'url': i['link']
                            }
            correct_list_vacancies.append(vacancy_info)
        return correct_list_vacancies

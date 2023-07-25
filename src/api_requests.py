import requests
import json
from abc import ABC, abstractmethod

QUANTITY_VACANCY = 100


class RequestsAPI(ABC):

    @abstractmethod
    def get_request(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_vacancies(self, *args, **kwargs):
        pass


class ParsingError(Exception):
    """Общий класс для API"""

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
        """Запрос по API"""
        req = requests.get(self.url, self.params)
        if req.status_code != 200:
            raise ParsingError(f'Ошибка получения вакансий. Код статуса: {req.status_code}')
        else:
            return req

    def get_vacancies(self, req):
        """Получаем список вакансий"""
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
                       "per_page": QUANTITY_VACANCY,
                       "page": 0,
                       }
        self.url = 'https://api.hh.ru/vacancies'
        self.key_with_vacancies = 'items'

    def edit_list_get_vacancies(self, vacancy_list):
        """ Редактируем список вакансий под свой формат"""
        correct_list_vacancies = []
        for i in vacancy_list[self.key_with_vacancies]:
            vacancy_info = {'api': 'HeadHunter',
                            'id': i['id'],
                            'company': i['employer']['name'],
                            'profession': i['name'],
                            'town': i['area']['name'],
                            'requirement': i['snippet']['requirement'],
                            'employment': i['employment']['name'],
                            'experience': i['experience']['name']
                            }
            if i['salary'] is None:
                vacancy_info['salary_from'] = None
                vacancy_info['salary_to'] = None
                vacancy_info['salary_currency'] = None
                vacancy_info['salary_mean'] = 0
            else:
                vacancy_info['salary_from'] = i['salary']['from']
                vacancy_info['salary_to'] = i['salary']['to']
                if i['salary']['from'] is None:
                    vacancy_info['salary_mean'] = i['salary']['to']
                elif i['salary']['to'] is None:
                    vacancy_info['salary_mean'] = i['salary']['from']
                else:
                    vacancy_info['salary_mean'] = int((i['salary']['from'] + i['salary']['to']) / 2)
                if i['salary']['currency'] == 'RUR':
                    vacancy_info['salary_currency'] = 'rub'
                else:
                    vacancy_info['salary_currency'] = i['salary']['currency']
            vacancy_info['url'] = f"https://www.hh.ru/vacancy/{vacancy_info['id'][4:]}"
            correct_list_vacancies.append(vacancy_info)
        return correct_list_vacancies


class SuperjobAPI(ParentAPI):

    def __init__(self, keyword):
        super().__init__()
        self.keyword = keyword
        self.params = {'count': QUANTITY_VACANCY,
                       'keyword': self.keyword}
        self.headers = {'X-Api-App-Id':
                        'v3.r.137693076.8c0a621f62c1bc4c0fadc3056207d620545fa9c6.'
                        '3a2d874af9ab61cef98ab134333dd3f98ecc486c'}
        self.url = 'https://api.superjob.ru/2.0/vacancies'
        self.key_with_vacancies = 'objects'

    def get_request(self):
        """Запрос по API"""
        req = requests.get(self.url, self.params, headers=self.headers)
        if req.status_code != 200:
            raise ParsingError(f'Ошибка получения вакансий. Код статуса: {req.status_code}')
        else:
            return req

    def edit_list_get_vacancies(self, vacancy_list):
        """ Редактируем список вакансий под свой формат"""
        correct_list_vacancies = []
        for i in vacancy_list[self.key_with_vacancies]:
            vacancy_info = {'api': 'Superjob',
                            'id': i['id'],
                            'company': i['firm_name'],
                            'profession': i['profession'],
                            'salary_currency': i['currency'],
                            'town': i['town']['title'],
                            'requirement': i['candidat'],
                            'employment': i['type_of_work']['title'],
                            'url': i['link']
                            }
            if i['experience']['title'] == 'Нет опыта':
                vacancy_info['experience'] = 'Без опыта'
            else:
                vacancy_info['experience'] = i['experience']['title']
            if i['payment_from'] == 0 and i['payment_to'] == 0:
                vacancy_info['salary_mean'] = 0
                vacancy_info['salary_from'] = None
                vacancy_info['salary_to'] = None
            elif i['payment_from'] == 0:
                vacancy_info['salary_from'] = None
                vacancy_info['salary_mean'] = i['payment_to']
                vacancy_info['salary_to'] = i['payment_to']
            elif i['payment_to'] == 0:
                vacancy_info['salary_from'] = i['payment_from']
                vacancy_info['salary_mean'] = i['payment_from']
                vacancy_info['salary_to'] = None
            else:
                vacancy_info['salary_from'] = i['payment_from']
                vacancy_info['salary_to'] = i['payment_to']
                vacancy_info['salary_mean'] = int((i['payment_from'] + i['payment_to']) / 2)
            correct_list_vacancies.append(vacancy_info)
        return correct_list_vacancies

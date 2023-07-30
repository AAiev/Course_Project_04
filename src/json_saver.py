import json
import os
from src.vacancy import Vacancy
from abc import ABC, abstractmethod


class JSON_abc(ABC):
    @abstractmethod
    def add_vacancy(self, *args, **kwargs):
        pass

    @abstractmethod
    def read_vacancies(self, *args, **kwargs):
        pass


class JSONSaver:
    def __init__(self):
        self.filename = 'list_vacansies.json'

    def add_vacancy(self, list_instances_vacancies):
        """ Сохраняет (перезаписывает) полученный список вакансий в JSON-файл"""
        data_list = []
        for i in list_instances_vacancies:
            dict_i = i.__dict__
            data_list.append(dict_i)
        path = os.path.join("data", self.filename)
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(data_list, file, ensure_ascii=False, indent=4)

    def read_vacancies(self):
        """Открывает JSON-файл с загруженными вакансиями"""
        path = os.path.join("data", self.filename)
        with open(path, 'r', encoding='utf-8') as file:
            load_vacancies = json.loads(file.read())
            list_load_vacancy = []
            for i in load_vacancies:
                vacancy = Vacancy(i)
                list_load_vacancy.append(vacancy)
            return list_load_vacancy

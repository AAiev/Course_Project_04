import json
import os
from operator import itemgetter
from src.vacancy import Vacancy


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

    @staticmethod
    def get_top_vacancy(num_top, load_vacancies):
        """
        Выдает ТОП вакансий по зп
        :param num_top: количество выводимых вакансий в ТОП. Либо меньше, если вакансий недостаточно
        :param load_vacancies: список вакансий для сортировки в ТОП
        :return: списко ТОП
        """
        top_list_sort = sorted(load_vacancies, key=itemgetter('salary_mean'), reverse=True)
        top_list_rub = []
        for i in top_list_sort:
            if i['salary_currency'] == 'rub':
                top_list_rub.append(i)
        if len(top_list_rub) < num_top:
            return top_list_rub
        else:
            return top_list_rub[:num_top]

    @staticmethod
    def get_vacancies_with_salary(load_vacancies):
        """Выводит вакансии, в которых указана ЗП"""
        vacancies_with_salary = []
        for i in load_vacancies:
            if i['salary_from'] is not None or i['salary_from'] is not None:
                vacancies_with_salary.append(i)
        return vacancies_with_salary

    @staticmethod
    def get_vacancies_without_experience(load_vacancies):
        """ Выдает вакансии с параметром - Без опыта работы"""
        vacancies_without_experience = [i for i in load_vacancies if i['experience'] == 'Без опыта']
        return vacancies_without_experience

    @staticmethod
    def get_vacancies_internship(load_vacancies):
        """ Выдает вакансии для стажировки"""
        vacancies_without_experience = [i for i in load_vacancies if 'стаж' in i['employment'].lower() or 'стаж' in i['profession'].lower()]
        return vacancies_without_experience

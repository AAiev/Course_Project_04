import pandas as pd
import os
from operator import itemgetter

from src.api_requests import HeadHunterAPI, SuperjobAPI
from src.vacancy import Vacancy


def get_result_choise_platform(num: int, user_keyword: str):
    """
    выдает откорректированный под наш формат список вакансий,
    в зависимости от вариантов ответа пользователя и заданного ключевого слова.
    :param num: int
    :param user_keyword: str
    :return: список в нужном формате
    """
    if num in [1, 2]:
        if num == 1:
            api = HeadHunterAPI(user_keyword)
        else:
            api = SuperjobAPI(user_keyword)
        request = api.get_request()
        vacancies = api.get_vacancies(request)
        correct_vacancies = api.edit_list_get_vacancies(vacancies)
        return correct_vacancies
    else:
        api_hh = HeadHunterAPI(user_keyword)
        api_sj = SuperjobAPI(user_keyword)
        request_hh = api_hh.get_request()
        request_sj = api_sj.get_request()
        vacancies_hh = api_hh.get_vacancies(request_hh)
        vacancies_sj = api_sj.get_vacancies(request_sj)
        correct_vacancies_hh = api_hh.edit_list_get_vacancies(vacancies_hh)
        correct_vacancies_sj = api_sj.edit_list_get_vacancies(vacancies_sj)
        correct_vacancies = correct_vacancies_hh + correct_vacancies_sj
        list_instances_vacancies = []
        for i in correct_vacancies:
            vacancy = Vacancy(i)
            list_instances_vacancies.append(vacancy)

        return list_instances_vacancies


def save_excel(list_vac):
    """ Сохраняет полученные вакансии в формате Excel"""
    user_answer = input("Сохранить вакансии в формате *.xlsx? ДА/НЕТ\n")
    if user_answer.upper() == 'YES' or user_answer.upper() == 'ДА':
        data_list = []
        for i in list_vac:
            dict_i = i.__dict__
            data_list.append(dict_i)
        file_to_excel = pd.DataFrame.from_dict(data_list)
        path = os.path.join('data', 'list_vac.xlsx')
        file_to_excel.to_excel(path)
        print(f'Файл {path} сохранен\n')
    else:
        print('Файл не сохранен\n')

def get_top_vacancy(num_top, load_vacancies):
    """
    Выдает ТОП вакансий по зп
    :param num_top: количество выводимых вакансий в ТОП. Либо меньше, если вакансий недостаточно
    :param load_vacancies: список вакансий для сортировки в ТОП
    :return: списко ТОП
    """
    data_list = []
    for i in load_vacancies:
        dict_i = i.__dict__
        data_list.append(dict_i)
    top_list_sort = sorted(data_list, key=itemgetter('salary_mean'), reverse=True)
    top_list_rub = []
    for i in top_list_sort:
        if i['salary_currency'] == 'rub':
            top_list_rub.append(i)
    top_list_rub_vac = []
    for i in top_list_rub:
        vac_emp = Vacancy(i)
        top_list_rub_vac.append(vac_emp)
    if len(top_list_rub_vac) < num_top:
        return top_list_rub_vac
    else:
        return top_list_rub_vac[:num_top]

def get_vacancies_with_salary(load_vacancies):
    """Выводит вакансии, в которых указана ЗП"""
    vacancies_with_salary = []
    for i in load_vacancies:
        if i.salary_from is not None or i.salary_to is not None:
            vacancies_with_salary.append(i)
    return vacancies_with_salary

def get_vacancies_without_experience(load_vacancies):
    """ Выдает вакансии с параметром - Без опыта работы"""
    vacancies_without_experience = []
    for i in load_vacancies:
        if i.experience == 'Без опыта':
            vacancies_without_experience.append(i)
    return vacancies_without_experience

def get_vacancies_internship(load_vacancies):
    """ Выдает вакансии для стажировки"""
    vacancies_without_experience = []
    for i in load_vacancies:
        if 'стаж' in i.employment.lower() or 'стаж' in i.profession.lower():
            vacancies_without_experience.append(i)
    return vacancies_without_experience
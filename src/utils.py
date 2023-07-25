from src.api_requests import HeadHunterAPI, SuperjobAPI
import pandas as pd
import os


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
        return correct_vacancies


def save_excel(list_vac):
    user_answer = input("Сохранить вакансии в формате *.xlsx? ДА/НЕТ\n")
    if user_answer.upper() == 'YES' or user_answer.upper() == 'ДА':
        file_to_excel = pd.DataFrame.from_dict(list_vac)
        path = os.path.join('data', 'list_vac.xlsx')
        file_to_excel.to_excel(path)
        print(f'Файл {path} сохранен\n')
    else:
        print('Файл не сохранен\n')

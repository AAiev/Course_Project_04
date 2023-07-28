from src.utils import get_result_choise_platform, save_excel
from src.json_saver import JSONSaver


def main():
    print('Привет!!!')
    while True:
        print('Выбири платформу для поиска вакансий')
        user_choise_platform = input('1 - HeadHunter\n'
                                     '2 - Superjob\n'
                                     '3 - Везде\n')
        if user_choise_platform in ['1', '2', '3']:
            break
        else:
            print('!!!Некорректное значение!!!\n')
    user_keyword = input('Введи ключевое слово для поиска вакансий: ')

    list_instances_vacancies = get_result_choise_platform(int(user_choise_platform), user_keyword)

    jsonsaver = JSONSaver()
    jsonsaver.add_vacancy(list_instances_vacancies)
    list_load_vacancy = jsonsaver.read_vacancies()
    while True:
        user_choise_param = input('Выбери один из вариантов фильтрации:\n'
                                  '1 - ТОП вакансий по зарплате в рублях\n'
                                  '2 - Все вакансии, где указана зарплата\n'
                                  '3 - Вакансии без опыта работы\n'
                                  '4 - Вывести вакансии для стажировки\n'
                                  '5 - Показать все вакансии\n'
                                  'stop - Пропустить фильтрацию\n')
        if user_choise_param == '1':
            while True:
                quantity_top = input('Сколько вакансий отобразить: 1-100?\n')
                if quantity_top.isdigit() and 0 < int(quantity_top) <= 100:
                    top_vacancies = jsonsaver.get_top_vacancy(int(quantity_top), list_load_vacancy)
                    if len(top_vacancies) == 0:
                        print('Нет вакансий, соответствующих заданным критериям.\n')
                    else:
                        [print(i) for i in top_vacancies]
                        save_excel(top_vacancies)
                    break
                else:
                    print('Некорректное значение. Попробуй еще раз.')
        elif user_choise_param == '2':
            vacancies_with_salary = jsonsaver.get_vacancies_with_salary(list_load_vacancy)
            if len(vacancies_with_salary) == 0:
                print('Нет вакансий, соответствующих заданным критериям.\n')
            else:
                [print(i) for i in vacancies_with_salary]
                save_excel(vacancies_with_salary)
        elif user_choise_param == '3':
            vacancies_without_experience = jsonsaver.get_vacancies_without_experience(list_load_vacancy)
            if len(vacancies_without_experience) == 0:
                print('Нет вакансий, соответствующих заданным критериям.\n')
            [print(i) for i in vacancies_without_experience]
            save_excel(vacancies_without_experience)
        elif user_choise_param == '4':
            vacancies_internship = jsonsaver.get_vacancies_internship(list_load_vacancy)
            if len(vacancies_internship) == 0:
                print('Нет вакансий, соответствующих заданным критериям.\n')
            else:
                [print(i) for i in vacancies_internship]
                save_excel(vacancies_internship)
        elif user_choise_param == '5':
            if len(list_load_vacancy) == 0:
                print('Нет вакансий, соответствующих заданным критериям.\n')
            else:
                [print(i) for i in list_load_vacancy]
                save_excel(list_load_vacancy)
        elif user_choise_param.lower() == 'stop' or user_choise_param.lower() == 'стоп':
            break
        else:
            print('Некорректное значение. Попробуй еще раз.')


if __name__ == '__main__':
    main()

class Vacancy:
    def __init__(self, dict_vacancy: dict):
        self.api = dict_vacancy['api']
        self.id = dict_vacancy['id']
        self.profession = dict_vacancy['profession']
        self.company = dict_vacancy['company']
        self.town = dict_vacancy['town']
        if dict_vacancy['salary_from'] is not None and dict_vacancy['salary_to'] is not None:
            self.salary = f"{dict_vacancy['salary_from']} - {dict_vacancy['salary_to']} {dict_vacancy['salary_currency']}"
        elif dict_vacancy['salary_from'] is None:
            self.salary = f"до {dict_vacancy['salary_to']} {dict_vacancy['salary_currency']}"
        elif dict_vacancy['salary_to'] is None:
            self.salary = f"от {dict_vacancy['salary_from']} {dict_vacancy['salary_currency']}"
        else:
            self.salary = 'Не указана'
        self.experience = dict_vacancy['experience']
        self.employment = dict_vacancy['employment']
        self.requirement = dict_vacancy['requirement']
        self.url = dict_vacancy['url']

    def __str__(self):
        return f'Вакансия от сервиса {self.api}. Город: {self.town}. id {self.id}\n' \
               f'Должность: {self.profession}. Компания/ИП: {self.company}.\n' \
               f'Зарплата: {self.salary}. {self.employment}.\n' \
               f'Опыт работы в должности: {self.experience}.' \
               f'{self.url}\n'

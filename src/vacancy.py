class Vacancy:
    def __init__(self, dict_vacancy: dict):
        self.api = dict_vacancy['api']
        self.id = dict_vacancy['id']
        self.profession = dict_vacancy['profession']
        self.company = dict_vacancy['company']
        self.town = dict_vacancy['town']
        self.salary_from = dict_vacancy['salary_from']
        self.salary_to = dict_vacancy['salary_to']
        self.salary_currency = dict_vacancy['salary_currency']
        self.salary_mean = dict_vacancy['salary_mean']
        self.experience = dict_vacancy['experience']
        self.employment = dict_vacancy['employment']
        self.requirement = dict_vacancy['requirement']
        self.url = dict_vacancy['url']

    def __str__(self):
        if self.salary_from is None and self.salary_to is None:
            self.salary = 'Не указана'
        elif self.salary_from is None:
            self.salary = f"до {self.salary_to} {self.salary_currency}"
        elif self.salary_to is None:
            self.salary = f"от {self.salary_from} {self.salary_currency}"
        else:
            self.salary = f"{self.salary_from} - {self.salary_to} {self.salary_currency}"
        return f'Вакансия от сервиса {self.api}. Город: {self.town}. id {self.id}\n' \
               f'Должность: {self.profession}. Компания/ИП: {self.company}.\n' \
               f'Зарплата: {self.salary}. {self.employment}.\n' \
               f'Опыт работы в должности: {self.experience}.' \
               f'{self.url}\n'

    def __gt__(self, other):
        return self.salary_mean > other.salary_mean

    def __le__(self, other):
        return self.salary_mean <= other.salary_mean

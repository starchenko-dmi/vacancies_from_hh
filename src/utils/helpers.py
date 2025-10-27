from typing import List
from src.models.vacancy import Vacancy

def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """Сортирует вакансии по убыванию зарплаты."""
    return sorted(vacancies, reverse=True)

def get_top_vacancies(vacancies: List[Vacancy], n: int) -> List[Vacancy]:
    """Возвращает топ N вакансий."""
    return vacancies[:n]

def filter_vacancies_by_keyword(vacancies: List[Vacancy], keywords: List[str]) -> List[Vacancy]:
    """Фильтрует вакансии по ключевым словам в описании."""
    if not keywords:
        return vacancies
    filtered = []
    for v in vacancies:
        desc = v.description.lower()
        if any(kw.lower() in desc for kw in keywords):
            filtered.append(v)
    return filtered
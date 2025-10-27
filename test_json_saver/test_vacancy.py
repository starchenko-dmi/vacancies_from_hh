import pytest
from src.models.vacancy import Vacancy

def test_vacancy_creation():
    v = Vacancy("Python Dev", "https://hh.ru/vacancy/123", 100000, 150000, "RUR", "Опыт 3 года")
    assert v.title == "Python Dev"
    assert v.salary_avg == 125000
    assert "3 года" in v.description

def test_vacancy_comparison():
    v1 = Vacancy("A", "https://a", 90000, None)
    v2 = Vacancy("B", "https://b", 100000, None)
    assert v1 < v2
    assert v2 > v1

def test_no_salary():
    v = Vacancy("Test", "https://test", None, None)
    assert v.salary_avg == 0
    assert v.get_salary_str() == "Зарплата не указана"

def test_invalid_url():
    with pytest.raises(ValueError):
        Vacancy("Bad", "not-url", 0, 0)

def test_empty_title():
    with pytest.raises(ValueError):
        Vacancy("", "https://a", 0, 0)
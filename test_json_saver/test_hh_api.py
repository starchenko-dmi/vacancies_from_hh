import pytest
from src.api.hh_api import HeadHunterAPI

def test_hh_connection():
    api = HeadHunterAPI()
    assert api._connect() is True

def test_get_vacancies():
    api = HeadHunterAPI()
    vacancies = api.get_vacancies("python", per_page=10)
    assert isinstance(vacancies, list)
    assert len(vacancies) <= 10
    if vacancies:
        assert "name" in vacancies[0]
        assert "alternate_url" in vacancies[0]
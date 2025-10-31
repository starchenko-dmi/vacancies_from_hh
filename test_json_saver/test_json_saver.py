import os
import json
from src.models.vacancy import Vacancy
from src.storage.json_saver import JSONSaver


def test_json_saver(tmp_path):
    file = tmp_path / "test_vacancies.json"
    saver = JSONSaver(str(file))

    v1 = Vacancy("Test", "https://hh.ru/vac/1", 100000, 150000)
    v2 = Vacancy("Test2", "https://hh.ru/vac/2", 120000, None)

    saver.add_vacancy(v1)
    saver.add_vacancy(v2)
    saver.add_vacancy(v1)  # дубликат — не должен добавиться

    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 2
    assert data[0]["title"] == "Test"
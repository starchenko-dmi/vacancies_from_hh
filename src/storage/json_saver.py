import json
import os
from typing import List
from src.storage.base_saver import BaseSaver
from src.models.vacancy import Vacancy

class JSONSaver(BaseSaver):
    """Класс для сохранения вакансий в JSON-файл."""

    def __init__(self, filename: str = "vacancies.json"):
        self.__filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Создаёт файл, если его нет."""
        if not os.path.exists(self.__filename):
            with open(self.__filename, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _read_file(self) -> List[dict]:
        """Читает данные из файла."""
        with open(self.__filename, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_file(self, data: List[dict]) -> None:
        """Записывает данные в файл."""
        with open(self.__filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет вакансию в файл (без дублей по URL)."""
        data = self._read_file()
        vacancy_dict = vacancy.to_dict()

        # Проверка на дубликат по URL
        if not any(v["url"] == vacancy_dict["url"] for v in data):
            data.append(vacancy_dict)
            self._write_file(data)

    def get_vacancies(self, **criteria) -> List[Vacancy]:
        """Возвращает вакансии по критериям (заглушка для расширения)."""
        data = self._read_file()
        vacancies = [Vacancy.from_dict(v) for v in data]

        # Пример фильтрации по ключевому слову в описании
        keyword = criteria.get("keyword")
        if keyword:
            vacancies = [
                v for v in vacancies
                if keyword.lower() in v.description.lower()
            ]

        return vacancies

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаляет вакансию по URL."""
        data = self._read_file()
        data = [v for v in data if v["url"] != vacancy.url]
        self._write_file(data)
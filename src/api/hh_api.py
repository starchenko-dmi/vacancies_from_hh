import requests
from typing import List
from src.api.base_api import BaseVacancyAPI

class HeadHunterAPI(BaseVacancyAPI):
    """Класс для взаимодействия с API hh.ru."""

    def __init__(self):
        self.__base_url = "https://api.hh.ru/vacancies"

    def _connect(self) -> bool:
        """Проверяет доступность API."""
        try:
            response = requests.get(self.__base_url, timeout=10)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def get_vacancies(self, search_query: str, per_page: int = 100) -> List[dict]:
        """Получает вакансии по ключевому слову."""
        if not self._connect():
            raise ConnectionError("Не удалось подключиться к API hh.ru")

        params = {
            "text": search_query,
            "per_page": min(per_page, 100),
            "area": 113,  # Россия
            "page": 0
        }

        response = requests.get(self.__base_url, params=params, timeout=10)
        if response.status_code != 200:
            raise RuntimeError(f"Ошибка API hh.ru: {response.status_code}")

        data = response.json()
        return data.get("items", [])
from abc import ABC, abstractmethod

class BaseVacancyAPI(ABC):
    """Абстрактный класс для работы с api платформы с вакансиями."""

    @abstractmethod
    def _connect(self) -> bool:
        """Приватный метод подключения к api."""
        pass

    @abstractmethod
    def get_vacancies(self, search_query: str) -> list[dict]:
        """Получение вакансий по поисковому запросу."""
        pass
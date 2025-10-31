from abc import ABC, abstractmethod
from src.models.vacancy import Vacancy

class BaseSaver(ABC):
    """Абстрактный класс для сохранения вакансий."""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        pass

    @abstractmethod
    def get_vacancies(self, **criteria) -> list[Vacancy]:
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        pass
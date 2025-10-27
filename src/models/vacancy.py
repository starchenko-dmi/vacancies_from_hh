from typing import Optional, Union, List, Dict

class Vacancy:
    """Класс для представления вакансии."""

    __slots__ = ("title", "url", "salary_from", "salary_to", "currency", "description")

    def __init__(
        self,
        title: str,
        url: str,
        salary_from: Optional[int],
        salary_to: Optional[int],
        currency: str = "RUR",
        description: str = ""
    ):
        self.title = self._validate_str(title, "Название вакансии")
        self.url = self._validate_url(url)
        self.salary_from = salary_from  # может быть None
        self.salary_to = salary_to      # может быть None
        self.currency = currency if currency else "RUR"
        self.description = description or ""

    @staticmethod
    def _validate_str(value: str, field_name: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field_name} не может быть пустым")
        return value.strip()

    @staticmethod
    def _validate_url(url: str) -> str:
        url = url.strip()
        if not url.startswith(("http://", "https://")):
            raise ValueError("Некорректный URL")
        return url

    @property
    def salary_avg(self) -> int:
        """Средняя зарплата (для сравнения и сортировки)."""
        from_val = self.salary_from or 0
        to_val = self.salary_to or 0
        if from_val and to_val:
            return (from_val + to_val) // 2
        return from_val or to_val

    def get_salary_str(self) -> str:
        """Возвращает представление зарплаты."""
        from_val = self.salary_from
        to_val = self.salary_to
        curr = self.currency or "RUR"

        if from_val is not None and to_val is not None:
            return f"от {from_val} до {to_val} {curr}"
        elif from_val is not None:
            return f"от {from_val} {curr}"
        elif to_val is not None:
            return f"до {to_val} {curr}"
        else:
            return "зарплата не указана"

    def __lt__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary_avg < other.salary_avg

    def __le__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary_avg <= other.salary_avg

    def __gt__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary_avg > other.salary_avg

    def __ge__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary_avg >= other.salary_avg

    def __eq__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary_avg == other.salary_avg

    def to_dict(self) -> dict:
        """Преобразует объект в словарь для сохранения."""
        return {
            "title": self.title,
            "url": self.url,
            "salary_from": self.salary_from,
            "salary_to": self.salary_to,
            "currency": self.currency,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Создаёт объект из словаря."""
        return cls(
            title=data["title"],
            url=data["url"],
            salary_from=data.get("salary_from"),
            salary_to=data.get("salary_to"),
            currency=data.get("currency", "RUR"),
            description=data.get("description", "")
        )

    @classmethod
    def cast_to_object_list(cls, vacancies_data: List[Dict]) -> List["Vacancy"]:
        """Преобразует список словарей от API в список объектов Vacancy."""
        vacancies = []
        for item in vacancies_data:
            try:
                salary = item.get("salary") or {}
                vacancy = cls(
                    title=item["name"],
                    url=item["alternate_url"],
                    salary_from=salary.get("from"),
                    salary_to=salary.get("to"),
                    currency=salary.get("currency", "RUR"),
                    description=item.get("snippet", {}).get("requirement", "")
                )
                vacancies.append(vacancy)
            except (KeyError, ValueError):
                # Пропускаем некорректные вакансии
                continue
        return vacancies
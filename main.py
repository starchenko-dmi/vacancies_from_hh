"""
Точка входа в программу.
Позволяет искать вакансии на hh.ru, фильтровать, сортировать и сохранять в JSON.
"""

from src.api.hh_api import HeadHunterAPI
from src.models.vacancy import Vacancy
from src.storage.json_saver import JSONSaver
from src.utils.helpers import (
    sort_vacancies,
    get_top_vacancies,
    filter_vacancies_by_keyword
)


def user_interaction():
    print("🔍 Парсер вакансий с hh.ru")
    print("=" * 50)

    search_query = input("Введите поисковый запрос: ").strip()
    if not search_query:
        print("❌ Поисковый запрос не может быть пустым.")
        return

    try:
        top_n = int(input("Сколько вакансий вывести в топе? (по зарплате): "))
        if top_n <= 0:
            raise ValueError
    except ValueError:
        print("⚠️ Некорректное число. Будет показано 5 вакансий.")
        top_n = 5

    keywords_input = input("Введите ключевые слова для фильтрации в описании (через пробел, или оставьте пустым): ").strip()
    keywords = keywords_input.split() if keywords_input else []

    print("\n⏳ Получаем данные с hh.ru...\n")

    try:
        hh_api = HeadHunterAPI()
        raw_vacancies = hh_api.get_vacancies(search_query, per_page=100)
        vacancies = Vacancy.cast_to_object_list(raw_vacancies)

        if not vacancies:
            print("❌ По вашему запросу вакансий не найдено.")
            return

        print(f"✅ Найдено {len(vacancies)} вакансий. Обрабатываем...")

        # Фильтрация по ключевым словам
        filtered = filter_vacancies_by_keyword(vacancies, keywords)
        if keywords and not filtered:
            print("⚠️ После фильтрации по ключевым словам вакансий не осталось.")
            return

        # Сортировка и выбор топа
        sorted_vac = sort_vacancies(filtered)
        top_vac = get_top_vacancies(sorted_vac, top_n)

        # Сохранение в файл
        saver = JSONSaver("vacancies.json")
        for v in top_vac:
            saver.add_vacancy(v)

        # Вывод результата
        print(f"\n🏆 Топ-{len(top_vac)} вакансий по запросу '{search_query}':\n")
        for i, v in enumerate(top_vac, 1):
            salary_str = v.get_salary_str()
            print(f"{i}. {v.title}")
            print(f"   💰 {salary_str}")
            print(f"   🌐 {v.url}")
            desc_preview = (v.description[:120] + "...") if len(v.description) > 120 else v.description
            print(f"   📝 {desc_preview}")
            print("-" * 70)

    except Exception as e:
        print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    user_interaction()
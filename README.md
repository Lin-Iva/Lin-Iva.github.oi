# FinTrack - система учета личных финансов

FinTrack - учебное Django-веб-приложение для учета личных финансов. Система позволяет:

- добавлять доходы и расходы;
- вести справочник категорий;
- формировать отчеты по категориям;
- отслеживать выполнение месячного бюджета;
- анализировать финансовое состояние на панели мониторинга.

## Стек

- Python 3.13
- Django 5.2
- SQLite 3
- Matplotlib для построения диаграмм
- HTML, CSS, Django Templates

## Структура репозитория

```text
finance_tracker_repo/
|- fintrack/                # настройки проекта Django
|- tracker/                 # бизнес-логика приложения
|  |- management/commands/  # команды, в том числе seed_demo
|  |- migrations/           # миграции БД
|  |- static/               # стили
|  |- templates/            # HTML-шаблоны
|  |- templatetags/         # пользовательские фильтры
|  |- admin.py              # регистрация в админ-панели
|  |- forms.py              # формы
|  |- models.py             # модели предметной области
|  |- services.py           # отчеты и графики
|  |- tests.py              # тесты
|  `- views.py              # представления
|- docs/
|  |- backup/               # логические резервные копии
|  `- screenshots/          # скриншоты интерфейса
|- manage.py
`- requirements.txt
```

## Быстрый старт

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Откройте `http://127.0.0.1:8000/dashboard/`.

## Логическая резервная копия базы

```bash
python manage.py dumpdata --indent 2 > docs/backup/finance_backup.json
```

## Тестирование

```bash
python manage.py test
```

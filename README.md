# Лабораторная работа №1 — FastAPI

Простой клиент-серверный сервис формирования меню столовой.

## Возможности

- общий список блюд;
- добавление, просмотр, изменение и удаление блюд;
- формирование меню по датам на ближайшие 31 день;
- добавление и удаление блюд из меню выбранного дня;
- REST API на FastAPI;
- валидация Pydantic;
- хранение данных in-memory;
- Swagger: `/docs`;
- три клиента: Python-скрипт, CLI и HTML + JavaScript.

## Установка

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск сервера

```bash
uvicorn main:app --reload
```

После запуска:

- веб-интерфейс: http://127.0.0.1:8000/
- Swagger: http://127.0.0.1:8000/docs

## Демонстрационный Python-клиент

При запущенном сервере:

```bash
python client.py
```

Скрипт последовательно демонстрирует CRUD: POST, GET, PUT и DELETE.

## CLI

```bash
python cli.py list
python cli.py add "Борщ" "Суп"
python cli.py get 1
python cli.py update 1 "Щи" "Суп"
python cli.py delete 1
python cli.py menu
python cli.py menu-add 2026-09-15 1
python cli.py menu-delete 2026-09-15 1
```

## Основные API-методы

### Блюда

- `GET /dishes` — список блюд
- `GET /dishes/{id}` — одно блюдо
- `POST /dishes` — добавить блюдо
- `PUT /dishes/{id}` — изменить блюдо
- `DELETE /dishes/{id}` — удалить блюдо

### Меню

- `GET /menu` — меню на ближайшие 31 день
- `GET /menu/{date}` — меню конкретного дня
- `POST /menu/{date}/dishes/{dish_id}` — добавить блюдо в меню дня
- `DELETE /menu/{date}/dishes/{dish_id}` — удалить блюдо из меню дня

Данные хранятся только в памяти приложения и очищаются при перезапуске сервера — это допустимо по условию лабораторной работы.

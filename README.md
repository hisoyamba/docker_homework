# 🐳 Docker ETL Pipeline

### Стек технологий

| Технология | Версия | Назначение |
|---|---|---|
| PostgreSQL | 17 | Исходная БД с демо-данными |
| PostgreSQL | 17 | Целевая БД |
| Python | 3.12 | ETL-скрипт |
| Docker Compose | 3 | Оркестрация контейнеров |
| pandas | latest | Обработка данных |
| SQLAlchemy | latest | Подключение к БД |

---

## 🗂️ Структура проекта

```
docker_homework/
├── docker-compose.yml          # оркестрация контейнеров
├── Dockerfile                  # образ Python ETL-скрипта
├── main.py                     # ETL-скрипт
├── requirements.txt            # зависимости Python
├── init_scripts/
│   ├── 00_create_db.sql        # создание базы данных demo
│   ├── demo-20250901-6m.sql    # дамп демо-базы (скачать отдельно)
│   └── zz_create_mart.sql      # создание витрины данных
└── README.md
```

---

## 🚀 Быстрый старт

### 1. Клонировать репозиторий

```bash
git clone https://github.com/hisoyamba/docker_homework.git
cd docker_homework
```

### 2. Скачать дамп базы данных

Скачать демо-базу авиакомпании с сайта PostgresPro:

🔗 https://postgrespro.ru/education/demodb

Положить файл в папку `init_scripts/`:

```bash
mv demo-20250901-6m.sql init_scripts/
```

### 3. Запустить проект

```bash
docker-compose up -d
```

Docker Compose автоматически:
1. Поднимет исходную PostgreSQL и загрузит дамп (~5-10 минут)
2. Создаст витрину `bookings.mart_route_sales`
3. Поднимет целевую PostgreSQL
4. Дождётся готовности обеих БД через healthcheck
5. Запустит Python ETL-скрипт

### 4. Проверить статус контейнеров

```bash
docker-compose ps
```

Все контейнеры должны быть в статусе `healthy` или `exited (0)`.

---

## 🔌 Подключение к базам данных

### Исходная БД (источник)

```
host:     localhost
port:     5432
user:     docker_pp
password: mypass
database: demo
```

### Целевая БД (приёмник)

```
host:     localhost
port:     5433
user:     docker_pp
password: mypass
database: postgres_db_target
```

---

## 📊 Витрина данных

Таблица `bookings.mart_route_sales` — агрегированная статистика продаж по маршрутам.

| Колонка | Тип | Описание |
|---|---|---|
| `route_no` | varchar | Номер маршрута |
| `departure_airport` | varchar | Код аэропорта вылета |
| `arrival_airport` | varchar | Код аэропорта прилёта |
| `dep_city` | varchar | Город вылета |
| `dep_country` | varchar | Страна вылета |
| `arr_city` | varchar | Город прилёта |
| `arr_country` | varchar | Страна прилёта |
| `flights_count` | bigint | Количество рейсов |
| `tickets_count` | bigint | Количество проданных билетов |
| `avg_price` | numeric | Средняя цена билета |
| `total_revenue` | numeric | Общая выручка |
| `min_price` | numeric | Минимальная цена билета |
| `max_price` | numeric | Максимальная цена билета |

---

## 📝 Логирование

Python ETL-скрипт логирует в stdout:

```
2026-04-21 10:00:00 - INFO - Начало загрузки данных
2026-04-21 10:00:01 - INFO - Подключение к источнику успешно
2026-04-21 10:00:02 - INFO - Прочитано строк из источника: 932
2026-04-21 10:00:03 - INFO - Подключение к приёмнику успешно
2026-04-21 10:00:04 - INFO - Загружено строк: 932
2026-04-21 10:00:04 - INFO - Время выполнения: 4.23 сек
```

Посмотреть логи:

```bash
docker-compose logs backend
```

---

## 🛑 Остановка проекта

```bash
# остановить контейнеры (данные сохранятся)
docker-compose down

# остановить и удалить все данные
docker-compose down -v
```

---

## 📚 Источник данных

Демо-база данных авиакомпании от [PostgresPro](https://postgrespro.ru/education/demodb) — учебная база с реальной структурой: рейсы, билеты, пассажиры, маршруты, аэропорты.

# Library Juls

Прототип электронной библиотеки с клиентской частью на Vue, сервером на FastAPI и поиском книг в каталоге ЛитРес.

**Авторы:** Рыбаков Я.В., Смирнова Ю.Е.<br>
**Группа:** P3269<br>
**Репозиторий:** <https://github.com/pistaha/libraryJuls-2>

## Оглавление

- [Цель и требования](#цель-работы)
- [Функциональность](#функциональность)
- [Архитектура и структура](#архитектура-приложения)
- [Запуск проекта](#локальный-запуск)
- [Скриншоты](#скриншоты)

## Цель работы

Разработать прототип веб-приложения электронной библиотеки, разделить его на frontend и backend, настроить клиентскую маршрутизацию, обмен данными через REST API, сборку Vite и контейнерный запуск.

## Выполнение требований

### Создание фронтэнд-составляющей. Часть 1

| Требование | Реализация |
| --- | --- |
| Создание Vite-проекта | Frontend создан на Vue 3 и Vite |
| Контейнер для frontend | Добавлены `frontend/Dockerfile` и конфигурация nginx |
| Настройка Vite | Настроены Vue-плагин, alias `@`, порт и proxy для `/api` |
| Production-сборка | Приложение собирается командой `npm run build` |
| Скриншоты приложения | Изображения размещены в `docs/imgs` и добавлены в отчет |
| Сервер с GET и POST | Backend на FastAPI предоставляет маршруты получения и добавления книг |
| Данные каталога | Начальные записи находятся в `data/books.json`, также используются данные ЛитРес |

### Создание фронтэнд-составляющей. Часть 2

| Требование | Реализация |
| --- | --- |
| Views и components | Реализованы страницы приложения и переиспользуемые компоненты |
| Клиентский router | Настроены основные маршруты, страница об авторах и обработка 404 |
| Связь frontend и backend | Frontend выполняет GET, POST и DELETE-запросы к FastAPI |
| Подключение внешнего каталога | Поиск ЛитРес выполняется через backend-прокси |

## Функциональность

- просмотр локального каталога;
- поиск по названию, автору, описанию и издательству;
- фильтрация по категории и статусу доступности;
- добавление и удаление книг;
- поиск электронных книг в ЛитРес;
- отображение обложки, автора, рейтинга и цены;
- переход на страницу книги в ЛитРес;
- сохранение найденной книги в локальный каталог;
- защита от повторного добавления одной книги из результатов поиска;
- переходы между разделами без перезагрузки страницы;
- отдельная страница для неизвестного маршрута.

## Используемые технологии

### Frontend

- Vue 3;
- Vue Router;
- Vite;
- JavaScript;
- HTML и CSS;
- Fetch API.

### Backend

- Python;
- FastAPI;
- Pydantic;
- HTTPX;
- Uvicorn;
- JSON-файл для хранения данных.

### Инфраструктура

- Docker;
- Docker Compose;
- nginx.

## Архитектура приложения

Frontend обращается только к маршрутам `/api`. В режиме разработки Vite перенаправляет запросы на FastAPI, а при контейнерном запуске эту задачу выполняет nginx.

Поиск во внешнем каталоге проходит по цепочке:

```text
Vue → /api/litres/search → FastAPI → API ЛитРес
```

Backend преобразует ответ ЛитРес в единый формат и передает клиенту только используемые поля. Запрос к внешнему сервису не выполняется напрямую из браузера.

## Структура проекта

```text
libraryJuls/
├── backend/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── data/
│   └── books.json
├── docs/
│   └── imgs/
│       ├── app-catalog.png
│       ├── app-home.png
│       └── app-litres.png
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AppFooter.vue
│   │   │   ├── AppHeader.vue
│   │   │   ├── BookItem.vue
│   │   │   ├── BookList.vue
│   │   │   └── LitresSearch.vue
│   │   ├── router/
│   │   │   └── index.js
│   │   ├── services/
│   │   │   └── booksApi.js
│   │   ├── views/
│   │   │   ├── AboutView.vue
│   │   │   ├── CatalogView.vue
│   │   │   ├── FavoritesView.vue
│   │   │   ├── HomeView.vue
│   │   │   ├── NotFoundView.vue
│   │   │   ├── PlaceholderView.vue
│   │   │   ├── ProfileView.vue
│   │   │   └── ReaderView.vue
│   │   ├── App.vue
│   │   └── main.js
│   ├── Dockerfile
│   ├── index.html
│   ├── nginx.conf
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml
└── README.md
```

## Маршруты frontend

| Маршрут | Назначение |
| --- | --- |
| `/` | Главная страница |
| `/catalog` | Локальный каталог и поиск ЛитРес |
| `/reader` | Раздел чтения |
| `/favorites` | Избранные книги |
| `/profile` | Профиль читателя |
| `/about` | Информация об авторах и проекте |
| `/:pathMatch(.*)*` | Страница 404 |

## REST API

| Метод | Маршрут | Назначение |
| --- | --- | --- |
| `GET` | `/api/health` | Проверка состояния сервера |
| `GET` | `/api/books` | Получение локального каталога |
| `POST` | `/api/books` | Добавление книги |
| `DELETE` | `/api/books/{book_id}` | Удаление книги |
| `GET` | `/api/litres/search?q={query}&limit={limit}` | Поиск книг в ЛитРес |

Тело POST-запроса:

```json
{
  "title": "Название книги",
  "author": "Автор",
  "description": "Описание",
  "publisher": "Издательство",
  "year": 2026,
  "category": "Категория",
  "available": true
}
```

## Локальный запуск

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Backend будет доступен по адресу <http://127.0.0.1:8000>. Интерактивная документация FastAPI находится по адресу <http://127.0.0.1:8000/docs>.

### Frontend

В отдельном окне терминала:

```bash
cd frontend
npm install
npm run dev
```

Frontend будет доступен по адресу <http://127.0.0.1:3000>.

Production-сборка frontend:

```bash
cd frontend
npm run build
```

## Запуск через Docker Compose

```bash
docker compose up --build
```

После запуска доступны:

- frontend: <http://localhost:3000>;
- backend: <http://localhost:8000>;
- Swagger UI: <http://localhost:8000/docs>.

Остановка контейнеров:

```bash
docker compose down
```

## Проверка API

```bash
curl http://127.0.0.1:8000/api/health
curl http://127.0.0.1:8000/api/books
curl --get http://127.0.0.1:8000/api/litres/search \
  --data-urlencode "q=Лев Толстой" \
  --data "limit=3"
```

## Скриншоты

### Главная страница

![Главная страница Library Juls](docs/imgs/app-home.png)

### Каталог библиотеки

![Каталог Library Juls](docs/imgs/app-catalog.png)

### Поиск и добавление книг из ЛитРес

![Поиск книг в ЛитРес](docs/imgs/app-litres.png)

## Результат

Создан прототип электронной библиотеки с клиентской маршрутизацией, локальным каталогом, серверным REST API и интеграцией с ЛитРес. Проект поддерживает запуск в режиме разработки и через Docker Compose.

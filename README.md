# Library Juls

Прототип SPA-приложения электронной библиотеки с frontend на Vue 3 + Vite и backend на FastAPI.

**Авторы:** Рыбаков Я.В., Смирнова Ю.Е.  
**Группа:** P3269  
**Дата выполнения:** 29.05.2026  
**Репозиторий:** <https://github.com/pistaha/libraryJuls>

## Цель работы

Создать прототип приложения электронной библиотеки, подготовить frontend-составляющую на Vite, реализовать backend с несколькими API-роутами, добавить моковые данные и настроить запуск через Docker.

## Что реализовано

- создан SPA frontend на `Vue 3` и `Vite`
- добавлен клиентский роутер на `vue-router`
- реализованы основные `views`: главная, каталог, читалка, избранное, профиль, об авторе и 404
- настроена сборка frontend через `npm run build`
- добавлен Dockerfile для frontend и nginx-конфигурация
- реализован backend на `FastAPI`
- добавлены API-роуты `GET`, `POST`, `DELETE`
- подключены моковые данные книг из `data/books.json`
- реализовано добавление книг через форму
- реализовано удаление книг из каталога
- добавлена фильтрация по поиску, категории и статусу доступности
- подготовлен общий запуск через `docker-compose.yml`

## Основные шаги выполнения

1. Создан frontend-проект с помощью `npm create vite@latest`.
2. Выбрана связка `Vue 3 + Vite` для реализации SPA-интерфейса электронной библиотеки.
3. Настроена структура frontend-приложения: views, shared components, router и service-модуль для API.
4. Добавлена форма управления каталогом: ввод названия, автора, описания, издательства, года, категории и статуса доступности.
5. Реализована фильтрация книг по поисковой строке, категории и статусу доступности.
6. Реализованы маршруты `/`, `/catalog`, `/reader`, `/favorites`, `/profile`, `/about` и fallback `/404`.
7. Настроен `vite.config.js`: задан порт dev-сервера и проксирование `/api` на backend.
8. Выполнена проверка production-сборки frontend командой `npm run build`.
9. Создан frontend-контейнер на основе `Dockerfile`: сборка приложения выполняется в Node.js, готовые статические файлы отдаются через nginx.
10. Добавлен `nginx.conf` для отдачи SPA и проксирования API-запросов на backend-контейнер.
11. Реализован backend-сервер на FastAPI.
12. Добавлены API-роуты для проверки сервера, получения списка книг, добавления книги и удаления книги.
13. Подготовлены моковые данные каталога в файле `data/books.json`.
14. Настроен `docker-compose.yml` для совместного запуска frontend и backend.
15. Сделаны скриншоты локально запущенного приложения и добавлены в `docs/imgs`.
16. Подготовлен отчет в `README.md` со структурой проекта, командами запуска, API и проверками.
17. Проект опубликован в отдельном GitHub-репозитории.

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
│       └── app-actions.png
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AppFooter.vue
│   │   │   ├── AppHeader.vue
│   │   │   ├── BookItem.vue
│   │   │   └── BookList.vue
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

## Скриншоты приложения

Скриншоты запущенного приложения через `npm run dev`:

![Каталог Library Juls](docs/imgs/app-catalog.png)

![Управление каталогом Library Juls](docs/imgs/app-actions.png)

## Frontend

Frontend расположен в папке `frontend`.

Основные команды:

```bash
cd frontend
npm install
npm run dev
```

Сборка production-версии:

```bash
cd frontend
npm run build
```

После запуска dev-сервера приложение доступно по адресу:

```text
http://127.0.0.1:3000/
```

Vite настроен так, чтобы запросы `/api` проксировались на backend:

```text
http://127.0.0.1:8000
```

### Маршруты frontend

| Роут | Раздел |
| --- | --- |
| `/` | Главная страница приложения |
| `/catalog` | Электронный каталог с данными из backend API |
| `/reader` | Заглушка раздела чтения |
| `/favorites` | Заглушка избранных книг |
| `/profile` | Заглушка профиля читателя |
| `/about` | Страница об авторе и проекте |

## Backend

Backend расположен в папке `backend` и реализован на FastAPI.

Запуск локально:

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

После запуска API доступно по адресу:

```text
http://127.0.0.1:8000
```

## API

| Метод | Роут | Назначение |
| --- | --- | --- |
| `GET` | `/api/health` | Проверка доступности backend |
| `GET` | `/api/books` | Получение списка книг |
| `POST` | `/api/books` | Добавление новой книги |
| `DELETE` | `/api/books/{book_id}` | Удаление книги по идентификатору |

Пример тела запроса для добавления книги:

```json
{
  "title": "Название книги",
  "author": "Автор",
  "description": "Описание книги",
  "publisher": "Издательство",
  "year": 2026,
  "category": "Категория",
  "available": true
}
```

Команды для проверки API:

```bash
curl http://127.0.0.1:8000/api/health
```

```bash
curl http://127.0.0.1:8000/api/books
```

```bash
curl -X POST http://127.0.0.1:8000/api/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Тестовая книга",
    "author": "Тестовый автор",
    "description": "Описание для проверки POST-запроса",
    "publisher": "Library Juls",
    "year": 2026,
    "category": "Тест",
    "available": true
  }'
```

```bash
curl -X DELETE http://127.0.0.1:8000/api/books/1
```

## Моковые данные

Данные каталога находятся в файле:

```text
data/books.json
```

Для каждой книги используются поля:

- `id`
- `title`
- `author`
- `description`
- `publisher`
- `year`
- `category`
- `available`
- `created_at`

## Docker

Для запуска всего приложения через Docker Compose:

```bash
docker compose build
docker compose up
```

После запуска контейнеров:

```text
Frontend: http://localhost:3000
Backend:  http://localhost:8000
```

`frontend/nginx.conf` проксирует запросы `/api/` во внутренний backend-сервис Docker Compose.

## Проверка выполнения

В рамках работы выполнены основные пункты задания:

- проект создан на основе Vite
- frontend собирается командой `npm run build`
- frontend запускается командой `npm run dev`
- добавлен Dockerfile для frontend
- настроена nginx-конфигурация для frontend-контейнера
- реализован backend-сервер FastAPI
- реализованы API-роуты для получения, добавления и удаления книг
- добавлены моковые данные
- подготовлен screenshot в `docs/imgs`
- проект опубликован в отдельном GitHub-репозитории

## Вывод

В результате был подготовлен прототип приложения Library Juls: электронный каталог книг с просмотром списка, добавлением, удалением и фильтрацией записей. Проект разделен на frontend и backend, поддерживает локальный запуск и контейнеризацию через Docker Compose.

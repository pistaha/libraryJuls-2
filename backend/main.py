from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import List

import httpx
from fastapi import FastAPI, HTTPException
from fastapi import Query
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = Path("/app/data") if Path("/app").exists() else BASE_DIR.parent / "data"
BOOKS_FILE = DATA_DIR / "books.json"
LITRES_API_URL = "https://api.litres.ru/foundation/api/search"
LITRES_SITE_URL = "https://www.litres.ru"
LITRES_CDN_URL = "https://cdn.litres.ru"


def current_timestamp() -> str:
    return datetime.now(UTC).isoformat()


def default_books() -> list[dict]:
    timestamp = current_timestamp()
    return [
        {
            "id": 1,
            "title": "Война и мир",
            "author": "Лев Толстой",
            "description": "Роман-эпопея о судьбах людей на фоне исторических событий начала XIX века.",
            "publisher": "Эксмо",
            "year": 2022,
            "category": "Художественная литература",
            "available": True,
            "created_at": timestamp,
        },
        {
            "id": 2,
            "title": "Python для сложных задач",
            "author": "Лучано Рамальо",
            "description": "Практическое руководство по современным возможностям Python.",
            "publisher": "Питер",
            "year": 2023,
            "category": "Программирование",
            "available": True,
            "created_at": timestamp,
        },
        {
            "id": 3,
            "title": "Архипелаг ГУЛАГ",
            "author": "Александр Солженицын",
            "description": "Документально-художественное исследование репрессивной системы СССР.",
            "publisher": "АСТ",
            "year": 2021,
            "category": "История",
            "available": False,
            "created_at": timestamp,
        },
    ]


def ensure_books_file() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not BOOKS_FILE.exists():
        BOOKS_FILE.write_text(
            json.dumps(default_books(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )


def load_books() -> list[dict]:
    ensure_books_file()
    return json.loads(BOOKS_FILE.read_text(encoding="utf-8"))


def save_books(books: list[dict]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    BOOKS_FILE.write_text(
        json.dumps(books, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


class Book(BaseModel):
    id: int
    title: str
    author: str
    description: str
    publisher: str
    year: int
    category: str
    available: bool
    favorite: bool = False
    booked: bool = False
    cover_url: str | None = None
    created_at: str


class BookCreate(BaseModel):
    title: str = Field(..., min_length=1)
    author: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    publisher: str = Field(..., min_length=1)
    year: int
    category: str = Field(..., min_length=1)
    available: bool = True
    favorite: bool = False
    booked: bool = False
    cover_url: str | None = None


class BookUpdate(BookCreate):
    pass


class LitresBook(BaseModel):
    id: int
    title: str
    author: str
    subtitle: str | None = None
    publisher: str | None = None
    year: int | None = None
    cover_url: str | None = None
    litres_url: str
    price: float | None = None
    currency: str | None = None
    rating: float | None = None
    is_free: bool = False


app = FastAPI(title="Library Juls API")


@app.on_event("startup")
def startup() -> None:
    ensure_books_file()


@app.get("/api/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/books", response_model=List[Book])
def get_books() -> list[dict]:
    return load_books()


@app.get("/api/books/{book_id}", response_model=Book)
def get_book(book_id: int) -> dict:
    books = load_books()
    for book in books:
        if book["id"] == book_id:
            return book

    raise HTTPException(status_code=404, detail="Book not found")


@app.post("/api/books", response_model=Book, status_code=201)
def create_book(payload: BookCreate) -> dict:
    books = load_books()
    next_id = max((book["id"] for book in books), default=0) + 1

    new_book = {
        "id": next_id,
        "title": payload.title,
        "author": payload.author,
        "description": payload.description,
        "publisher": payload.publisher,
        "year": payload.year,
        "category": payload.category,
        "available": payload.available,
        "favorite": payload.favorite,
        "booked": payload.booked,
        "cover_url": payload.cover_url,
        "created_at": current_timestamp(),
    }

    books.append(new_book)
    save_books(books)
    return new_book


@app.put("/api/books/{book_id}", response_model=Book)
def update_book(book_id: int, payload: BookUpdate) -> dict:
    books = load_books()

    for index, book in enumerate(books):
        if book["id"] == book_id:
            updated_book = {
                **book,
                "title": payload.title,
                "author": payload.author,
                "description": payload.description,
                "publisher": payload.publisher,
                "year": payload.year,
                "category": payload.category,
                "available": payload.available,
                "favorite": payload.favorite,
                "booked": payload.booked,
                "cover_url": payload.cover_url,
            }
            books[index] = updated_book
            save_books(books)
            return updated_book

    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/api/books/{book_id}")
def delete_book(book_id: int) -> dict[str, int]:
    books = load_books()
    updated_books = [book for book in books if book["id"] != book_id]

    if len(updated_books) == len(books):
        raise HTTPException(status_code=404, detail="Book not found")

    save_books(updated_books)
    return {"deleted_id": book_id}


@app.get("/api/litres/search", response_model=List[LitresBook])
async def search_litres_books(
    q: str = Query(..., min_length=2, max_length=100),
    limit: int = Query(8, ge=1, le=20),
) -> list[dict]:
    """Search text books on LitRes and return a stable subset of its response."""
    params = [("q", q), ("types", "text_book"), ("limit", str(limit))]

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(LITRES_API_URL, params=params)
            response.raise_for_status()
            payload = response.json()
    except (httpx.HTTPError, ValueError) as error:
        raise HTTPException(status_code=502, detail="LitRes API is unavailable") from error

    if payload.get("status") != 200:
        raise HTTPException(status_code=502, detail="LitRes API returned an error")

    results = []
    for search_item in payload.get("payload", {}).get("data", []):
        if search_item.get("type") != "text_book":
            continue

        item = search_item.get("instance", {})
        persons = item.get("persons") or []
        authors = [person["full_name"] for person in persons if person.get("role") == "author"]
        publishers = [person["full_name"] for person in persons if person.get("role") == "publisher"]
        prices = item.get("prices") or {}
        rating = item.get("rating") or {}
        released_at = item.get("last_released_at") or ""
        cover_path = item.get("cover_url")
        book_path = item.get("url") or ""

        results.append(
            {
                "id": item["id"],
                "title": item.get("title") or "Без названия",
                "author": ", ".join(authors) or "Автор не указан",
                "subtitle": item.get("subtitle"),
                "publisher": ", ".join(publishers) or None,
                "year": int(released_at[:4]) if released_at[:4].isdigit() else None,
                "cover_url": f"{LITRES_CDN_URL}{cover_path}" if cover_path else None,
                "litres_url": f"{LITRES_SITE_URL}{book_path}",
                "price": prices.get("final_price"),
                "currency": prices.get("currency"),
                "rating": rating.get("rated_avg"),
                "is_free": bool(item.get("is_free")),
            }
        )

    return results

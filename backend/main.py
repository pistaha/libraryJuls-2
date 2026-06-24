from __future__ import annotations

import json
import sqlite3
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
DATABASE_FILE = DATA_DIR / "books.db"
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
            "favorite": False,
            "booked": False,
            "cover_url": None,
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
            "favorite": False,
            "booked": False,
            "cover_url": None,
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
            "favorite": False,
            "booked": False,
            "cover_url": None,
            "created_at": timestamp,
        },
    ]


def get_connection() -> sqlite3.Connection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_FILE)
    connection.row_factory = sqlite3.Row
    return connection


def row_to_book(row: sqlite3.Row) -> dict:
    book = dict(row)
    book["available"] = bool(book["available"])
    book["favorite"] = bool(book["favorite"])
    book["booked"] = bool(book["booked"])
    return book


def ensure_database() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                description TEXT NOT NULL,
                publisher TEXT NOT NULL,
                year INTEGER NOT NULL,
                category TEXT NOT NULL,
                available INTEGER NOT NULL DEFAULT 1,
                favorite INTEGER NOT NULL DEFAULT 0,
                booked INTEGER NOT NULL DEFAULT 0,
                cover_url TEXT,
                created_at TEXT NOT NULL
            )
            """
        )

        books_count = connection.execute("SELECT COUNT(*) FROM books").fetchone()[0]
        if books_count:
            return

        seed_books = default_books()
        if BOOKS_FILE.exists():
            seed_books = json.loads(BOOKS_FILE.read_text(encoding="utf-8"))

        connection.executemany(
            """
            INSERT INTO books (
                id, title, author, description, publisher, year, category,
                available, favorite, booked, cover_url, created_at
            )
            VALUES (
                :id, :title, :author, :description, :publisher, :year, :category,
                :available, :favorite, :booked, :cover_url, :created_at
            )
            """,
            [
                {
                    **book,
                    "available": int(book.get("available", True)),
                    "favorite": int(book.get("favorite", False)),
                    "booked": int(book.get("booked", False)),
                    "cover_url": book.get("cover_url"),
                }
                for book in seed_books
            ],
        )


def load_books() -> list[dict]:
    ensure_database()
    with get_connection() as connection:
        rows = connection.execute("SELECT * FROM books ORDER BY id").fetchall()
    return [row_to_book(row) for row in rows]


def find_book(book_id: int) -> dict | None:
    ensure_database()
    with get_connection() as connection:
        row = connection.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    return row_to_book(row) if row else None


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
    ensure_database()


@app.get("/api/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/books", response_model=List[Book])
def get_books() -> list[dict]:
    return load_books()


@app.get("/api/books/{book_id}", response_model=Book)
def get_book(book_id: int) -> dict:
    book = find_book(book_id)
    if book:
        return book

    raise HTTPException(status_code=404, detail="Book not found")


@app.post("/api/books", response_model=Book, status_code=201)
def create_book(payload: BookCreate) -> dict:
    ensure_database()
    created_at = current_timestamp()

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO books (
                title, author, description, publisher, year, category,
                available, favorite, booked, cover_url, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                payload.title,
                payload.author,
                payload.description,
                payload.publisher,
                payload.year,
                payload.category,
                int(payload.available),
                int(payload.favorite),
                int(payload.booked),
                payload.cover_url,
                created_at,
            ),
        )

    created_book = find_book(cursor.lastrowid)
    if created_book:
        return created_book

    raise HTTPException(status_code=500, detail="Book was not created")


@app.put("/api/books/{book_id}", response_model=Book)
def update_book(book_id: int, payload: BookUpdate) -> dict:
    ensure_database()
    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE books
            SET title = ?,
                author = ?,
                description = ?,
                publisher = ?,
                year = ?,
                category = ?,
                available = ?,
                favorite = ?,
                booked = ?,
                cover_url = ?
            WHERE id = ?
            """,
            (
                payload.title,
                payload.author,
                payload.description,
                payload.publisher,
                payload.year,
                payload.category,
                int(payload.available),
                int(payload.favorite),
                int(payload.booked),
                payload.cover_url,
                book_id,
            ),
        )

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Book not found")

    updated_book = find_book(book_id)
    if updated_book:
        return updated_book

    raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/api/books/{book_id}")
def delete_book(book_id: int) -> dict[str, int]:
    ensure_database()
    with get_connection() as connection:
        cursor = connection.execute("DELETE FROM books WHERE id = ?", (book_id,))

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Book not found")

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

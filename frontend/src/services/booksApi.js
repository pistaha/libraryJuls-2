async function requestJson(url, options = {}) {
  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export function fetchBooks() {
  return requestJson('/api/books');
}

export function fetchBook(bookId) {
  return requestJson(`/api/books/${bookId}`);
}

export function createBook(bookPayload) {
  return requestJson('/api/books', {
    method: 'POST',
    body: JSON.stringify(bookPayload),
  });
}

export function updateBook(bookId, bookPayload) {
  return requestJson(`/api/books/${bookId}`, {
    method: 'PUT',
    body: JSON.stringify(bookPayload),
  });
}

export function removeBook(bookId) {
  return requestJson(`/api/books/${bookId}`, {
    method: 'DELETE',
  });
}

export function searchLitresBooks(query, limit = 8) {
  const params = new URLSearchParams({ q: query, limit: String(limit) });
  return requestJson(`/api/litres/search?${params.toString()}`);
}

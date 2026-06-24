<template>
  <LitresSearch :catalog-books="books" :import-book="importBook" />
  <BookList
    :books="books"
    :loading="loading"
    :error-message="errorMessage"
    @delete-book="deleteBook"
    @toggle-status="toggleBookStatus"
    @toggle-favorite="toggleFavorite"
    @toggle-booked="toggleBooked"
  />
</template>

<script setup>
import { onMounted, ref } from 'vue';
import BookList from '@/components/BookList.vue';
import LitresSearch from '@/components/LitresSearch.vue';
import { createBook, fetchBooks, removeBook, updateBook } from '@/services/booksApi';

const books = ref([]);
const loading = ref(false);
const errorMessage = ref('');

async function loadBooks() {
  loading.value = true;
  errorMessage.value = '';

  try {
    books.value = await fetchBooks();
  } catch (error) {
    errorMessage.value = 'Не удалось загрузить каталог книг.';
  } finally {
    loading.value = false;
  }
}

async function importBook(bookPayload) {
  errorMessage.value = '';

  try {
    const createdBook = await createBook(bookPayload);
    books.value = [...books.value, createdBook];
    return createdBook;
  } catch (error) {
    throw new Error('Book import failed');
  }
}

async function updateLocalBook(book, patch) {
  errorMessage.value = '';

  try {
    const updatedBook = await updateBook(book.id, {
      title: book.title,
      author: book.author,
      description: book.description,
      publisher: book.publisher,
      year: book.year,
      category: book.category,
      available: book.available,
      favorite: book.favorite || false,
      booked: book.booked || false,
      cover_url: book.cover_url || null,
      ...patch,
    });

    books.value = books.value.map((item) => {
      return item.id === updatedBook.id ? updatedBook : item;
    });
  } catch (error) {
    errorMessage.value = 'Не удалось обновить книгу.';
  }
}

function toggleBookStatus(book) {
  updateLocalBook(book, { available: !book.available });
}

function toggleFavorite(book) {
  updateLocalBook(book, { favorite: !book.favorite });
}

function toggleBooked(book) {
  updateLocalBook(book, { booked: !book.booked });
}

async function deleteBook(bookId) {
  errorMessage.value = '';

  try {
    await removeBook(bookId);
    books.value = books.value.filter((book) => book.id !== bookId);
  } catch (error) {
    errorMessage.value = 'Не удалось удалить книгу.';
  }
}

onMounted(loadBooks);
</script>

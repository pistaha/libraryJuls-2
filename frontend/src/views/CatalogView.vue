<template>
  <BookList
    :books="books"
    :loading="loading"
    :error-message="errorMessage"
    @add-book="addBook"
    @delete-book="deleteBook"
  />
</template>

<script setup>
import { onMounted, ref } from 'vue';
import BookList from '@/components/BookList.vue';
import { createBook, fetchBooks, removeBook } from '@/services/booksApi';

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

async function addBook(bookPayload) {
  errorMessage.value = '';

  try {
    const createdBook = await createBook(bookPayload);
    books.value = [...books.value, createdBook];
  } catch (error) {
    errorMessage.value = 'Не удалось добавить книгу.';
  }
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

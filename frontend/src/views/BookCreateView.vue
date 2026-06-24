<template>
  <LayoutCard title="Новая книга" eyebrow="Форма">
    <template #meta>
      Заполните карточку книги по основным полям библиографического описания.
    </template>

    <p v-if="errorMessage" class="form-message">{{ errorMessage }}</p>
    <BookForm submit-label="Создать книгу" @submit-book="saveBook" />
  </LayoutCard>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import BookForm from '@/components/BookForm.vue';
import LayoutCard from '@/components/LayoutCard.vue';
import { createBook } from '@/services/booksApi';

const router = useRouter();
const errorMessage = ref('');

async function saveBook(bookPayload) {
  errorMessage.value = '';

  try {
    await createBook(bookPayload);
    router.push({ name: 'books' });
  } catch (error) {
    errorMessage.value = 'Не удалось сохранить книгу.';
  }
}
</script>

<style scoped>
.form-message {
  margin: 0 0 18px;
  padding: 14px;
  border-radius: 10px;
  background: #fee2e2;
  color: #991b1b;
  font-weight: 700;
}
</style>

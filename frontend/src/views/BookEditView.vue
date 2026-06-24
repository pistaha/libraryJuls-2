<template>
  <LayoutCard title="Редактирование книги" eyebrow="Форма">
    <template #meta>
      Измените нужные поля и сохраните карточку в каталоге.
    </template>

    <p v-if="errorMessage" class="form-message form-message--error">
      {{ errorMessage }}
    </p>
    <p v-else-if="loading" class="form-message">
      Загружаем книгу...
    </p>
    <BookForm
      v-else-if="book"
      :initial-book="book"
      submit-label="Сохранить изменения"
      @submit-book="saveBook"
    />
  </LayoutCard>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import BookForm from '@/components/BookForm.vue';
import LayoutCard from '@/components/LayoutCard.vue';
import { fetchBook, updateBook } from '@/services/booksApi';

const route = useRoute();
const router = useRouter();
const book = ref(null);
const loading = ref(false);
const errorMessage = ref('');

async function loadBook() {
  loading.value = true;
  errorMessage.value = '';

  try {
    book.value = await fetchBook(route.params.id);
  } catch (error) {
    errorMessage.value = 'Книга не найдена.';
  } finally {
    loading.value = false;
  }
}

async function saveBook(bookPayload) {
  errorMessage.value = '';

  try {
    await updateBook(route.params.id, bookPayload);
    router.push({ name: 'books' });
  } catch (error) {
    errorMessage.value = 'Не удалось обновить книгу.';
  }
}

onMounted(loadBook);
</script>

<style scoped>
.form-message {
  margin: 0 0 18px;
  padding: 14px;
  border-radius: 10px;
  background: #eef6ff;
  color: #334e68;
  font-weight: 700;
}

.form-message--error {
  background: #fee2e2;
  color: #991b1b;
}
</style>

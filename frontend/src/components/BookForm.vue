<template>
  <form class="book-form" @submit.prevent="submitBook">
    <label>
      Заголовок
      <input v-model.trim="form.title" required type="text" placeholder="Название книги">
    </label>

    <label>
      Автор
      <input v-model.trim="form.author" required type="text" placeholder="Автор">
    </label>

    <label>
      Описание
      <textarea v-model.trim="form.description" required rows="4" placeholder="Краткое описание"></textarea>
    </label>

    <label>
      Обложка jpg
      <input accept=".jpg,.jpeg,image/jpeg" type="file" @change="selectCover">
    </label>

    <label>
      Издательство
      <select v-model="form.publisher" required>
        <option value="" disabled>Выберите издательство</option>
        <option v-for="publisher in publishers" :key="publisher" :value="publisher">
          {{ publisher }}
        </option>
      </select>
    </label>

    <label>
      Год издания
      <input v-model.number="form.year" required min="1450" :max="currentYear" type="number">
    </label>

    <fieldset>
      <legend>Возрастной рейтинг</legend>
      <label v-for="rating in ageRatings" :key="rating" class="book-form__radio">
        <input v-model="form.category" required type="radio" :value="rating">
        {{ rating }}
      </label>
    </fieldset>

    <label class="book-form__checkbox">
      <input v-model="form.available" type="checkbox">
      Книга в наличии
    </label>

    <label class="book-form__checkbox">
      <input v-model="form.favorite" type="checkbox">
      В избранном
    </label>

    <label class="book-form__checkbox">
      <input v-model="form.booked" type="checkbox">
      Забронирована
    </label>

    <p v-if="validationMessage" class="book-form__message">
      {{ validationMessage }}
    </p>

    <div class="book-form__actions">
      <button type="submit">{{ submitLabel }}</button>
      <RouterLink to="/books">Отмена</RouterLink>
    </div>
  </form>
</template>

<script setup>
import { reactive, ref, watch } from 'vue';

const props = defineProps({
  initialBook: {
    type: Object,
    default: null,
  },
  submitLabel: {
    type: String,
    default: 'Сохранить книгу',
  },
});

const emit = defineEmits(['submit-book']);

const currentYear = new Date().getFullYear();
const publishers = [
  'АСТ',
  'Эксмо',
  'Питер',
  'O\'Reilly Media',
  'Prentice Hall',
  'Литрес Классика',
  'ИТМОНЯ',
  'тайгер',
];
const ageRatings = ['0+', '6+', '12+', '16+', '18+'];
const validationMessage = ref('');

const form = reactive(createForm(props.initialBook));

watch(
  () => props.initialBook,
  (book) => {
    Object.assign(form, createForm(book));
  },
);

function createForm(book) {
  return {
    title: book?.title || '',
    author: book?.author || '',
    description: book?.description || '',
    publisher: book?.publisher || '',
    year: book?.year || currentYear,
    category: ageRatings.includes(book?.category) ? book.category : '12+',
    available: book?.available ?? true,
    favorite: book?.favorite ?? false,
    booked: book?.booked ?? false,
    cover_url: book?.cover_url || '',
  };
}

function selectCover(event) {
  const [file] = event.target.files;

  if (!file) {
    return;
  }

  if (!file.type.includes('jpeg')) {
    validationMessage.value = 'Для обложки нужен файл jpg.';
    event.target.value = '';
    return;
  }

  form.cover_url = file.name;
  validationMessage.value = '';
}

function submitBook() {
  if (form.title.length < 2 || form.author.length < 2) {
    validationMessage.value = 'Название и автор должны быть длиннее одного символа.';
    return;
  }

  if (form.year > currentYear) {
    validationMessage.value = 'Год издания не может быть больше текущего.';
    return;
  }

  validationMessage.value = '';
  emit('submit-book', {
    title: form.title,
    author: form.author,
    description: form.description,
    publisher: form.publisher,
    year: Number(form.year),
    category: form.category,
    available: form.available,
    favorite: form.favorite,
    booked: form.booked,
    cover_url: form.cover_url || null,
  });
}
</script>

<style scoped>
.book-form {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}

.book-form label,
.book-form fieldset {
  display: grid;
  gap: 7px;
  color: #486581;
  font-size: 0.88rem;
  font-weight: 700;
}

.book-form input,
.book-form textarea,
.book-form select {
  width: 100%;
  border: 1px solid rgba(98, 125, 152, 0.34);
  border-radius: 8px;
  padding: 10px 12px;
  color: #102a43;
  font: inherit;
  background: #fff;
}

.book-form textarea,
.book-form fieldset,
.book-form__message,
.book-form__actions {
  grid-column: 1 / -1;
}

.book-form textarea {
  resize: vertical;
}

.book-form fieldset {
  display: flex;
  flex-wrap: wrap;
  gap: 14px 24px;
  margin: 0;
  padding: 14px;
  border: 1px solid rgba(98, 125, 152, 0.24);
  border-radius: 10px;
}

.book-form legend {
  padding: 0 6px;
}

.book-form__radio,
.book-form__checkbox {
  display: flex !important;
  grid-template-columns: none !important;
  align-items: center;
  gap: 8px !important;
  min-width: 72px;
  white-space: nowrap;
}

.book-form__radio input,
.book-form__checkbox input {
  width: 18px;
  height: 18px;
}

.book-form__message {
  margin: 0;
  padding: 12px 14px;
  border-radius: 10px;
  background: #fee2e2;
  color: #991b1b;
  font-weight: 700;
}

.book-form__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.book-form__actions button,
.book-form__actions a {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 42px;
  padding: 10px 16px;
  border-radius: 8px;
  font: inherit;
  font-weight: 800;
}

.book-form__actions button {
  border: 0;
  color: #fff;
  background: #0f766e;
  cursor: pointer;
}

.book-form__actions a {
  border: 1px solid rgba(15, 118, 110, 0.28);
  color: #0f766e;
}

@media (max-width: 760px) {
  .book-form {
    grid-template-columns: 1fr;
  }

  .book-form fieldset {
    grid-template-columns: repeat(2, max-content);
  }
}
</style>

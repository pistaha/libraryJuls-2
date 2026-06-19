<template>
  <section class="litres-search">
    <div class="litres-search__heading">
      <div>
        <p class="litres-search__eyebrow">Каталог ЛитРес</p>
        <h2>Поиск книг в ЛитРес</h2>
      </div>
      <a href="https://www.litres.ru" target="_blank" rel="noopener noreferrer">Перейти в ЛитРес</a>
    </div>

    <form class="litres-search__form" @submit.prevent="search">
      <label>
        Название или автор
        <input
          v-model.trim="query"
          minlength="2"
          required
          type="search"
          placeholder="Название книги или автор"
        >
      </label>
      <button :disabled="loading" type="submit">
        {{ loading ? 'Ищем…' : 'Найти в ЛитРес' }}
      </button>
    </form>

    <p v-if="errorMessage" class="litres-search__message litres-search__message--error">
      {{ errorMessage }}
    </p>
    <p v-else-if="statusMessage" class="litres-search__message litres-search__message--success">
      {{ statusMessage }}
    </p>
    <p v-else-if="searched && !books.length" class="litres-search__message">
      По вашему запросу книги не найдены.
    </p>

    <div v-if="books.length" class="litres-search__grid">
      <article v-for="book in books" :key="book.id" class="litres-card">
        <img v-if="book.cover_url" :src="book.cover_url" :alt="`Обложка книги «${book.title}»`">
        <div v-else class="litres-card__cover">Нет обложки</div>

        <div class="litres-card__body">
          <h3>{{ book.title }}</h3>
          <p class="litres-card__author">{{ book.author }}</p>
          <p v-if="book.subtitle" class="litres-card__subtitle">{{ book.subtitle }}</p>
          <div class="litres-card__meta">
            <span v-if="book.rating">★ {{ book.rating }}</span>
            <span v-if="book.is_free">Бесплатно</span>
            <span v-else-if="book.price">{{ formatPrice(book.price, book.currency) }}</span>
          </div>
          <div class="litres-card__actions">
            <button
              type="button"
              :disabled="importingBookId === book.id || isBookInCatalog(book)"
              @click="saveBook(book)"
            >
              {{ importButtonText(book.id) }}
            </button>
            <a :href="book.litres_url" target="_blank" rel="noopener noreferrer">Открыть</a>
          </div>
        </div>
      </article>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue';
import { searchLitresBooks } from '@/services/booksApi';

const props = defineProps({
  importBook: {
    type: Function,
    required: true,
  },
  catalogBooks: {
    type: Array,
    required: true,
  },
});

const query = ref('');
const books = ref([]);
const loading = ref(false);
const searched = ref(false);
const errorMessage = ref('');
const statusMessage = ref('');
const importingBookId = ref(null);

async function search() {
  loading.value = true;
  searched.value = false;
  errorMessage.value = '';
  statusMessage.value = '';

  try {
    books.value = await searchLitresBooks(query.value);
    searched.value = true;
  } catch (error) {
    books.value = [];
    errorMessage.value = 'ЛитРес сейчас недоступен.';
  } finally {
    loading.value = false;
  }
}

async function saveBook(book) {
  importingBookId.value = book.id;
  errorMessage.value = '';
  statusMessage.value = '';

  try {
    await props.importBook({
      title: book.title,
      author: book.author,
      description: book.subtitle || book.title,
      publisher: book.publisher || 'ЛитРес',
      year: book.year || new Date().getFullYear(),
      category: 'ЛитРес',
      available: true,
    });
    statusMessage.value = `«${book.title}» добавлена в библиотеку.`;
  } catch (error) {
    errorMessage.value = `Не удалось добавить «${book.title}».`;
  } finally {
    importingBookId.value = null;
  }
}

function importButtonText(bookId) {
  if (importingBookId.value === bookId) {
    return 'Добавляем…';
  }
  const book = books.value.find((item) => item.id === bookId);
  if (book && isBookInCatalog(book)) {
    return 'Добавлено';
  }
  return 'Добавить в библиотеку';
}

function isBookInCatalog(book) {
  const title = book.title.trim().toLocaleLowerCase('ru-RU');
  const author = book.author.trim().toLocaleLowerCase('ru-RU');

  return props.catalogBooks.some((catalogBook) => {
    return catalogBook.title.trim().toLocaleLowerCase('ru-RU') === title
      && catalogBook.author.trim().toLocaleLowerCase('ru-RU') === author;
  });
}

function formatPrice(price, currency) {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: currency || 'RUB',
    maximumFractionDigits: 2,
  }).format(price);
}
</script>

<style scoped>
.litres-search {
  margin-bottom: 24px;
  padding: 28px;
  border-radius: 16px;
  background: linear-gradient(135deg, #fff7ed 0%, #ffffff 58%);
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
}

.litres-search__heading {
  display: flex;
  justify-content: space-between;
  align-items: end;
  gap: 16px;
  margin-bottom: 20px;
}

.litres-search__eyebrow {
  margin: 0 0 8px;
  color: #c2410c;
  font-size: 0.8rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.litres-search h2,
.litres-card h3 {
  margin: 0;
  color: #102a43;
}

.litres-search__heading > a {
  color: #c2410c;
  font-weight: 700;
}

.litres-search__form {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 12px;
  align-items: end;
}

.litres-search__form label {
  display: grid;
  gap: 7px;
  color: #486581;
  font-size: 0.86rem;
  font-weight: 700;
}

.litres-search__form input {
  width: 100%;
  min-height: 42px;
  padding: 10px 12px;
  border: 1px solid rgba(194, 65, 12, 0.28);
  border-radius: 8px;
  color: #102a43;
  background: #fff;
  font: inherit;
}

.litres-search__form button,
.litres-card__actions button {
  min-height: 42px;
  padding: 10px 16px;
  border: 0;
  border-radius: 8px;
  color: #fff;
  background: #c2410c;
  font: inherit;
  font-weight: 700;
  cursor: pointer;
}

.litres-search__form button:disabled {
  cursor: wait;
  opacity: 0.65;
}

.litres-search__message {
  margin: 18px 0 0;
  color: #52606d;
  font-weight: 600;
}

.litres-search__message--error {
  color: #991b1b;
}

.litres-search__message--success {
  color: #047857;
}

.litres-search__grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 16px;
  margin-top: 22px;
}

.litres-card {
  display: grid;
  grid-template-columns: 92px 1fr;
  gap: 14px;
  min-width: 0;
  padding: 14px;
  border: 1px solid rgba(194, 65, 12, 0.16);
  border-radius: 14px;
  background: #fff;
}

.litres-card img,
.litres-card__cover {
  width: 92px;
  height: 132px;
  border-radius: 8px;
  object-fit: cover;
  background: #ffedd5;
}

.litres-card__cover {
  display: grid;
  place-items: center;
  padding: 8px;
  color: #9a3412;
  text-align: center;
  font-size: 0.75rem;
}

.litres-card__body {
  min-width: 0;
}

.litres-card h3 {
  font-size: 1rem;
}

.litres-card__author,
.litres-card__subtitle {
  margin: 6px 0 0;
  color: #0f766e;
  font-size: 0.88rem;
}

.litres-card__subtitle {
  color: #627d98;
}

.litres-card__meta,
.litres-card__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
  margin-top: 12px;
}

.litres-card__meta {
  color: #92400e;
  font-size: 0.85rem;
  font-weight: 700;
}

.litres-card__actions button {
  min-height: 36px;
  padding: 7px 10px;
  font-size: 0.78rem;
}

.litres-card__actions button:disabled {
  cursor: default;
  opacity: 0.68;
}

.litres-card__actions a {
  color: #c2410c;
  font-size: 0.84rem;
  font-weight: 700;
}

@media (max-width: 640px) {
  .litres-search {
    padding: 22px 18px;
  }

  .litres-search__heading,
  .litres-search__form {
    grid-template-columns: 1fr;
  }

  .litres-search__heading {
    align-items: start;
    flex-direction: column;
  }
}
</style>

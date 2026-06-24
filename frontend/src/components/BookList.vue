<template>
  <LayoutCard title="Книги библиотеки" eyebrow="Каталог">
    <template #actions>
      <RouterLink class="catalog__button" to="/books/new">Добавить книгу</RouterLink>
    </template>

    <template #meta="{ title }">
      {{ title }}: найдено {{ filteredBooks.length }} из {{ books.length }}
    </template>

    <div class="filters">
      <label>
        Поиск
        <input v-model.trim="searchQuery" type="search" placeholder="Название, автор, описание">
      </label>
      <label>
        Категория
        <select v-model="categoryFilter">
          <option value="">Все категории</option>
          <option v-for="category in categories" :key="category" :value="category">
            {{ category }}
          </option>
        </select>
      </label>
      <label>
        Статус
        <select v-model="statusFilter">
          <option value="all">Все книги</option>
          <option value="available">В наличии</option>
          <option value="busy">Выданные</option>
          <option value="favorite">Избранные</option>
          <option value="booked">Забронированные</option>
        </select>
      </label>
      <label>
        Сортировка
        <select v-model="sortType">
          <option value="created_desc">Сначала новые</option>
          <option value="title_asc">По алфавиту</option>
        </select>
      </label>
    </div>

    <p v-if="filterMessage" class="catalog__hint">{{ filterMessage }}</p>

    <p v-if="errorMessage" class="catalog__message catalog__message--error">
      {{ errorMessage }}
    </p>
    <p v-else-if="loading" class="catalog__message">
      Загрузка каталога...
    </p>
    <p v-else-if="!filteredBooks.length" class="catalog__message">
      По выбранным условиям книг нет.
    </p>

    <div v-else class="catalog__grid">
      <BookItem
        v-for="book in filteredBooks"
        :key="book.id"
        :book="book"
        @delete-book="$emit('delete-book', book.id)"
        @toggle-status="$emit('toggle-status', book)"
        @toggle-favorite="$emit('toggle-favorite', book)"
        @toggle-booked="$emit('toggle-booked', book)"
      />
    </div>
  </LayoutCard>
</template>

<script setup>
import { computed, ref, watch } from 'vue';
import BookItem from '@/components/BookItem.vue';
import LayoutCard from '@/components/LayoutCard.vue';

const props = defineProps({
  books: {
    type: Array,
    required: true,
  },
  loading: {
    type: Boolean,
    default: false,
  },
  errorMessage: {
    type: String,
    default: '',
  },
});

defineEmits(['delete-book', 'toggle-status', 'toggle-favorite', 'toggle-booked']);

const searchQuery = ref('');
const categoryFilter = ref('');
const statusFilter = ref('all');
const sortType = ref('created_desc');
const filterMessage = ref('');

const categories = computed(() => {
  return [...new Set(props.books.map((book) => book.category).filter(Boolean))].sort((a, b) => {
    return a.localeCompare(b, 'ru');
  });
});

const filteredBooks = computed(() => {
  const query = searchQuery.value.toLocaleLowerCase('ru-RU');

  const filtered = props.books.filter((book) => {
    const matchesSearch = !query || [
      book.title,
      book.author,
      book.description,
      book.publisher,
    ].some((value) => value.toLocaleLowerCase('ru-RU').includes(query));

    const matchesCategory = !categoryFilter.value || book.category === categoryFilter.value;
    const matchesStatus =
      statusFilter.value === 'all' ||
      (statusFilter.value === 'available' && book.available) ||
      (statusFilter.value === 'busy' && !book.available) ||
      (statusFilter.value === 'favorite' && book.favorite) ||
      (statusFilter.value === 'booked' && book.booked);

    return matchesSearch && matchesCategory && matchesStatus;
  });

  return [...filtered].sort((firstBook, secondBook) => {
    if (sortType.value === 'title_asc') {
      return firstBook.title.localeCompare(secondBook.title, 'ru');
    }

    return new Date(secondBook.created_at) - new Date(firstBook.created_at);
  });
});

watch([searchQuery, categoryFilter, statusFilter, sortType], () => {
  filterMessage.value = 'Фильтр обновлен.';
});
</script>

<style scoped>
.filters {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 14px;
  margin-bottom: 18px;
}

.filters label {
  display: grid;
  gap: 7px;
  color: #486581;
  font-size: 0.86rem;
  font-weight: 700;
}

.filters input,
.filters select {
  width: 100%;
  border: 1px solid rgba(98, 125, 152, 0.34);
  border-radius: 8px;
  padding: 10px 12px;
  color: #102a43;
  font: inherit;
  background: #ffffff;
}

.catalog__button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 42px;
  padding: 10px 16px;
  border-radius: 8px;
  background: #0f766e;
  color: #fff;
  font-weight: 800;
}

.catalog__hint {
  margin: 0 0 14px;
  color: #627d98;
  font-size: 0.92rem;
  font-weight: 700;
}

.catalog__message {
  margin: 0;
  padding: 18px;
  border-radius: 12px;
  background: #eef6ff;
  color: #334e68;
  font-weight: 600;
}

.catalog__message--error {
  background: #fee2e2;
  color: #991b1b;
}

.catalog__grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 18px;
  margin-top: 12px;
}

@media (max-width: 980px) {
  .filters {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .filters {
    grid-template-columns: 1fr;
  }
}
</style>

<template>
  <article class="book-card">
    <div class="book-card__top">
      <span class="book-card__category">{{ book.category }}</span>
      <span :class="['book-card__badge', book.available ? 'is-available' : 'is-busy']">
        {{ book.available ? 'В наличии' : 'Выдана' }}
      </span>
    </div>

    <h3>{{ book.title }}</h3>
    <p class="book-card__author">{{ book.author }}</p>
    <p class="book-card__description">{{ book.description }}</p>

    <dl class="book-card__meta">
      <div>
        <dt>Издательство</dt>
        <dd>{{ book.publisher }}</dd>
      </div>
      <div>
        <dt>Год</dt>
        <dd>{{ book.year }}</dd>
      </div>
    </dl>

    <div class="book-card__flags">
      <span v-if="book.favorite">В избранном</span>
      <span v-if="book.booked">Забронирована</span>
      <span v-if="book.cover_url">Обложка: {{ book.cover_url }}</span>
    </div>

    <div class="book-card__actions">
      <RouterLink :to="{ name: 'book-edit', params: { id: book.id } }">
        Редактировать
      </RouterLink>
      <button type="button" @click="$emit('toggle-status', book)">
        Изменить статус
      </button>
      <button type="button" @click="$emit('toggle-favorite', book)">
        {{ book.favorite ? 'Убрать сердечко' : 'В избранное' }}
      </button>
      <button type="button" @click="$emit('toggle-booked', book)">
        {{ book.booked ? 'Снять бронь' : 'Забронировать' }}
      </button>
      <button class="book-card__delete" type="button" @click="$emit('delete-book')">
        Удалить
      </button>
    </div>
  </article>
</template>

<script setup>
defineProps({
  book: {
    type: Object,
    required: true,
  },
});

defineEmits(['delete-book', 'toggle-status', 'toggle-favorite', 'toggle-booked']);
</script>

<style scoped>
.book-card {
  display: grid;
  align-content: start;
  padding: 20px;
  border: 1px solid rgba(148, 163, 184, 0.22);
  border-radius: 16px;
  background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
}

.book-card__top {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  align-items: center;
}

.book-card__category {
  font-size: 0.82rem;
  color: #486581;
}

.book-card__badge {
  padding: 6px 10px;
  border-radius: 999px;
  font-size: 0.78rem;
  font-weight: 700;
}

.book-card__badge.is-available {
  background: #d1fae5;
  color: #065f46;
}

.book-card__badge.is-busy {
  background: #fee2e2;
  color: #991b1b;
}

.book-card h3 {
  margin: 16px 0 8px;
  color: #102a43;
}

.book-card__author {
  margin: 0 0 12px;
  color: #0f766e;
  font-weight: 600;
}

.book-card__description {
  margin: 0 0 18px;
  color: #52606d;
}

.book-card__meta {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin: 0;
}

.book-card__meta div {
  padding-top: 12px;
  border-top: 1px solid rgba(148, 163, 184, 0.2);
}

.book-card__meta dt {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #829ab1;
}

.book-card__meta dd {
  margin: 6px 0 0;
  color: #334e68;
  font-weight: 600;
}

.book-card__flags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 16px;
}

.book-card__flags span {
  padding: 5px 8px;
  border-radius: 999px;
  background: #eef6ff;
  color: #334e68;
  font-size: 0.78rem;
  font-weight: 700;
}

.book-card__actions {
  display: grid;
  gap: 9px;
  margin-top: 18px;
}

.book-card__actions a,
.book-card__actions button {
  width: 100%;
  min-height: 38px;
  border: 1px solid rgba(15, 118, 110, 0.24);
  border-radius: 8px;
  padding: 9px 10px;
  background: #ffffff;
  color: #0f766e;
  font: inherit;
  font-weight: 700;
  text-align: center;
  cursor: pointer;
}

.book-card__actions a:hover,
.book-card__actions button:hover {
  background: #ecfdf5;
}

.book-card__actions .book-card__delete {
  border-color: rgba(153, 27, 27, 0.18);
  background: #fff5f5;
  color: #991b1b;
}

.book-card__actions .book-card__delete:hover {
  background: #fee2e2;
}
</style>

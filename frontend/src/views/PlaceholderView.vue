<template>
  <section class="placeholder">
    <p>{{ eyebrow }}</p>
    <h1>{{ title }}</h1>
    <span>{{ description }}</span>
    <RouterLink to="/books">перейти в каталог</RouterLink>
  </section>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true,
  },
  eyebrow: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    required: true,
  },
});
</script>

<style scoped>
.placeholder {
  min-height: 360px;
  padding: 30px;
  border-radius: 16px;
  background: #ffffff;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
  display: grid;
  align-content: center;
  justify-items: start;
  gap: 14px;
}

.placeholder p {
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #486581;
  font-size: 0.8rem;
  font-weight: 700;
}

.placeholder h1 {
  margin: 0;
  color: #102a43;
}

.placeholder span {
  max-width: 680px;
  color: #334e68;
}

.placeholder a {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 42px;
  margin-top: 8px;
  padding: 10px 16px;
  border-radius: 8px;
  background: #0f766e;
  color: #ffffff;
  font-weight: 700;
}
</style>

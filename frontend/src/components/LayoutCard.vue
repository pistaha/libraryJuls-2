<template>
  <section class="layout-card">
    <div class="layout-card__header">
      <div>
        <p v-if="eyebrow" class="layout-card__eyebrow">{{ eyebrow }}</p>
        <h1>{{ title }}</h1>
      </div>
      <div v-if="$slots.actions" class="layout-card__actions">
        <slot name="actions" />
      </div>
    </div>

    <div v-if="$slots.meta" class="layout-card__meta">
      <slot name="meta" :title="title" :eyebrow="eyebrow" />
    </div>

    <slot />
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
    default: '',
  },
});
</script>

<style scoped>
.layout-card {
  padding: 28px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.94);
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
}

.layout-card__header {
  display: flex;
  justify-content: space-between;
  align-items: end;
  gap: 16px;
  margin-bottom: 22px;
}

.layout-card__eyebrow {
  margin: 0 0 8px;
  color: #486581;
  font-size: 0.8rem;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.layout-card h1 {
  margin: 0;
  color: #102a43;
}

.layout-card__actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 10px;
}

.layout-card__meta {
  margin: -8px 0 20px;
  color: #627d98;
  font-size: 0.95rem;
}

@media (max-width: 720px) {
  .layout-card {
    padding: 22px 18px;
  }

  .layout-card__header {
    flex-direction: column;
    align-items: start;
  }

  .layout-card__actions {
    justify-content: flex-start;
  }
}
</style>

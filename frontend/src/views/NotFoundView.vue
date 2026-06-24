<template>
  <section class="not-found">
    <div class="not-found__content">
      <div class="not-found__image-wrap">
        <img
          class="not-found__image"
          :src="sadImage"
          alt="Грустная картинка для страницы 404"
        >
      </div>

      <div class="not-found__text">
        <p class="not-found__eyebrow">Ошибка 404</p>
        <h1>Страница потерялась</h1>
        <p>
          Похоже, такой страницы нет в электронной библиотеке.
          Возможно, ссылка устарела или раздел еще не добавлен.
        </p>

        <div class="not-found__actions">
          <RouterLink class="not-found__button not-found__button--primary" to="/">
            На главную
          </RouterLink>
          <RouterLink class="not-found__button" to="/books">
            В каталог
          </RouterLink>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import sadImage from '@/assets/sad-404.jpg';
</script>

<style scoped>
.not-found {
  min-height: calc(100vh - 170px);
  display: grid;
  place-items: center;
  padding: 28px 0;
}

.not-found__content {
  width: min(980px, 100%);
  display: grid;
  grid-template-columns: minmax(240px, 340px) minmax(0, 1fr);
  align-items: center;
  gap: 42px;
  padding: 44px;
  border: 1px solid rgba(71, 85, 105, 0.12);
  border-radius: 20px;
  background:
    linear-gradient(135deg, rgba(226, 232, 240, 0.95), rgba(255, 255, 255, 0.94)),
    radial-gradient(circle at 20% 10%, rgba(148, 163, 184, 0.24), transparent 32%);
  box-shadow: 0 24px 60px rgba(15, 23, 42, 0.16);
}

.not-found__image-wrap {
  position: relative;
  max-width: 340px;
  margin: 0 auto;
  padding: 18px;
  border-radius: 22px;
  background: #f8fafc;
  box-shadow: inset 0 0 0 1px rgba(148, 163, 184, 0.24);
}

.not-found__image-wrap::before {
  content: "404";
  position: absolute;
  top: -34px;
  left: -22px;
  z-index: 0;
  color: rgba(100, 116, 139, 0.12);
  font-size: 6rem;
  font-weight: 900;
  line-height: 1;
}

.not-found__image {
  position: relative;
  z-index: 1;
  display: block;
  width: 100%;
  border-radius: 16px;
  filter: grayscale(16%) saturate(82%) brightness(0.96);
}

.not-found__text {
  display: grid;
  gap: 18px;
}

.not-found__eyebrow {
  margin: 0;
  color: #64748b;
  font-size: 0.9rem;
  font-weight: 800;
  letter-spacing: 0.12em;
  text-transform: uppercase;
}

.not-found h1 {
  margin: 0;
  color: #102a43;
  font-size: clamp(3.2rem, 7vw, 6rem);
  line-height: 0.95;
}

.not-found__text p:not(.not-found__eyebrow) {
  max-width: 560px;
  margin: 0;
  color: #52606d;
  font-size: 1.15rem;
}

.not-found__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 8px;
}

.not-found__button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  padding: 11px 18px;
  border: 1px solid rgba(15, 118, 110, 0.26);
  border-radius: 8px;
  color: #0f766e;
  font-weight: 800;
}

.not-found__button--primary {
  border-color: #0f766e;
  color: #fff;
  background: #0f766e;
}

@media (max-width: 780px) {
  .not-found {
    min-height: auto;
    padding: 18px 0;
  }

  .not-found__content {
    grid-template-columns: 1fr;
    gap: 26px;
    padding: 26px 20px;
    text-align: center;
  }

  .not-found__image-wrap {
    width: min(260px, 100%);
  }

  .not-found__actions {
    justify-content: center;
  }
}
</style>

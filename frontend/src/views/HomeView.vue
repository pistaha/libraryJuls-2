<template>
  <section class="home">
    <div class="home__intro">
      <p class="eyebrow">Электронная библиотека</p>
      <h1>Library Juls</h1>
      <p>
        SPA-прототип для учета книг, управления электронным каталогом и перехода
        между основными разделами библиотечного сервиса.
      </p>
      <div class="home__actions">
        <RouterLink class="button button--primary" to="/catalog">Открыть каталог</RouterLink>
        <RouterLink class="button" to="/about">Об авторе</RouterLink>
      </div>
    </div>

    <div class="home__grid" aria-label="Разделы приложения">
      <RouterLink class="home-card" to="/catalog">
        <span>Каталог</span>
        <strong>Поиск, фильтры и добавление книг через API</strong>
      </RouterLink>
      <RouterLink class="home-card" to="/reader">
        <span>Читалка</span>
        <strong>Заглушка будущего раздела для чтения электронных книг</strong>
      </RouterLink>
      <RouterLink class="home-card" to="/favorites">
        <span>Избранное</span>
        <strong>Заглушка списка сохраненных книг пользователя</strong>
      </RouterLink>
      <RouterLink class="home-card" to="/profile">
        <span>Профиль</span>
        <strong>Заглушка личного кабинета читателя</strong>
      </RouterLink>
    </div>
  </section>
</template>

<style scoped>
.home {
  display: grid;
  gap: 28px;
}

.home__intro {
  padding: 32px;
  border-radius: 16px;
  background: #ffffff;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
}

.eyebrow {
  margin: 0 0 12px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  font-size: 0.8rem;
  color: #486581;
}

h1 {
  margin: 0;
  font-size: clamp(2.2rem, 4vw, 3.8rem);
  line-height: 1.05;
  color: #102a43;
}

.home__intro p:not(.eyebrow) {
  max-width: 720px;
  margin: 16px 0 0;
  color: #334e68;
  font-size: 1.05rem;
}

.home__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 22px;
}

.button,
.home-card {
  border-radius: 8px;
  text-decoration: none;
}

.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 42px;
  padding: 10px 16px;
  border: 1px solid rgba(15, 118, 110, 0.28);
  color: #0f766e;
  font-weight: 700;
}

.button--primary {
  background: #0f766e;
  color: #ffffff;
}

.home__grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
}

.home-card {
  display: grid;
  gap: 10px;
  min-height: 150px;
  padding: 20px;
  background: #ffffff;
  border: 1px solid rgba(148, 163, 184, 0.24);
  box-shadow: 0 12px 26px rgba(15, 23, 42, 0.06);
}

.home-card span {
  color: #0f766e;
  font-weight: 800;
}

.home-card strong {
  color: #334e68;
  line-height: 1.4;
}

@media (max-width: 900px) {
  .home__grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .home__intro {
    padding: 24px 20px;
  }

  .home__grid {
    grid-template-columns: 1fr;
  }
}
</style>

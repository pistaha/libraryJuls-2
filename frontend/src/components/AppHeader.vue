<template>
  <header class="header">
    <div class="header__inner">
      <div>
        <p class="header__label">Library Juls</p>
      </div>
      <nav class="header__nav">
        <RouterLink to="/">Главная</RouterLink>
        <RouterLink to="/catalog">Каталог</RouterLink>
        <RouterLink to="/reader">Читалка</RouterLink>
        <RouterLink to="/favorites">Избранное</RouterLink>
        <RouterLink to="/profile">Профиль</RouterLink>
        <RouterLink to="/about">Об авторе</RouterLink>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.header {
  position: sticky;
  top: 0;
  z-index: 10;
  backdrop-filter: blur(12px);
  background: rgba(247, 250, 252, 0.82);
  border-bottom: 1px solid rgba(15, 23, 42, 0.08);
}

.header__inner {
  width: min(1120px, calc(100% - 32px));
  margin: 0 auto;
  padding: 18px 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.header__label {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 700;
  color: #102a43;
}

.header__subtitle {
  font-size: 0.92rem;
  color: #627d98;
}

.header__nav {
  display: flex;
  flex-wrap: wrap;
  justify-content: end;
  gap: 8px;
}

.header__nav a {
  padding: 8px 10px;
  border-radius: 8px;
  font-weight: 600;
  color: #0f766e;
}

.header__nav a.router-link-active {
  background: rgba(15, 118, 110, 0.1);
}

@media (max-width: 768px) {
  .header__inner {
    width: min(100% - 20px, 1120px);
    align-items: flex-start;
    padding: 14px 0;
  }

  .header__nav {
    justify-content: flex-start;
  }
}
</style>

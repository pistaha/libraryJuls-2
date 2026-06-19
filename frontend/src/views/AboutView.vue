<template>
  <section class="page">
    <p class="page__eyebrow">О проекте</p>
    <h1>Об авторе</h1>
    <div class="page__content">
      <p><strong>Авторы:</strong> Рыбаков Я.В., Смирнова Ю.Е.</p>
      <p><strong>Группа:</strong> P3269</p>
      <p>
        Library Juls объединяет собственный каталог библиотеки с поиском книг в ЛитРес.
      </p>
    </div>
  </section>
</template>

<style scoped>
.page {
  padding: 30px;
  border-radius: 16px;
  background: #ffffff;
  box-shadow: 0 18px 40px rgba(15, 23, 42, 0.08);
}

.page__eyebrow {
  margin: 0 0 10px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #486581;
  font-size: 0.8rem;
  font-weight: 700;
}

h1 {
  margin: 0 0 18px;
  color: #102a43;
}

.page__content {
  display: grid;
  gap: 12px;
  max-width: 760px;
  color: #334e68;
}

.page__content p {
  margin: 0;
}
</style>

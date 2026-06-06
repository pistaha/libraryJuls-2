<template>
  <footer class="footer">
    <div class="footer__inner">
      <p>Library Juls</p>
      <span>Vue 3 + Vue Router + FastAPI</span>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  margin-top: auto;
  border-top: 1px solid rgba(15, 23, 42, 0.08);
  background: rgba(255, 255, 255, 0.7);
}

.footer__inner {
  width: min(1120px, calc(100% - 32px));
  margin: 0 auto;
  padding: 18px 0 28px;
  display: flex;
  justify-content: space-between;
  gap: 12px;
  color: #627d98;
}

.footer__inner p {
  margin: 0;
  font-weight: 600;
  color: #334e68;
}

.footer__inner span {
  color: #627d98;
}

@media (max-width: 768px) {
  .footer__inner {
    width: min(100% - 20px, 1120px);
    flex-direction: column;
  }
}
</style>

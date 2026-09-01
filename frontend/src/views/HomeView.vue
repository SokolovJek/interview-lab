<template>
  <div class="home-page">
    <div class="welcome-card">
      <h1>👋 Добро пожаловать, {{ authStore.user?.username || 'User' }}!</h1>
      <p>Вы успешно вошли в систему.</p>

      <div class="quick-actions">
        <router-link to="/practice" class="action-card">
          <span class="icon">🎯</span>
          <h3>Практика</h3>
          <p>Проверьте свои знания</p>
        </router-link>

        <router-link to="/dashboard" class="action-card">
          <span class="icon">📊</span>
          <h3>Дашборд</h3>
          <p>Просмотр статистики</p>
        </router-link>

        <router-link to="/profile" class="action-card">
          <span class="icon">👤</span>
          <h3>Профиль</h3>
          <p>Управление аккаунтом</p>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
</script>

<style scoped>
.home-page {
  max-width: 900px;
  margin: 0 auto;
}

.welcome-card {
  background: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.welcome-card h1 {
  color: #2c3e50;
  margin-bottom: 8px;
}

.welcome-card p {
  color: #6b7a8f;
  font-size: 16px;
  margin-bottom: 32px;
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.action-card {
  background: #f8fafc;
  padding: 24px;
  border-radius: 12px;
  text-decoration: none;
  color: #2c3e50;
  transition: all 0.2s;
  border: 1.5px solid transparent;
}

.action-card:hover {
  border-color: #4a6cf7;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.action-card .icon {
  font-size: 32px;
  display: block;
  margin-bottom: 8px;
}

.action-card h3 {
  margin: 0 0 4px 0;
  font-size: 18px;
}

.action-card p {
  margin: 0;
  font-size: 14px;
  color: #6b7a8f;
}
</style>

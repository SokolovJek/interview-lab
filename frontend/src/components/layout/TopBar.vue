<template>
  <header class="topbar">
    <div class="topbar-container">
      <!-- Левая часть: Логотип -->
      <div class="topbar-left">
        <router-link to="/" class="logo">
          <span class="logo-icon">🚀</span>
          <span class="logo-text">MyApp</span>
        </router-link>
      </div>

      <!-- Центральная часть: Навигация (только для авторизованных) -->
      <nav v-if="authStore.token" class="topbar-nav">
        <router-link to="/" class="nav-link">Главная</router-link>
        <router-link to="/practice" class="nav-link">🎯 Практика</router-link>
        <router-link to="/dashboard" class="nav-link">📊 Дашборд</router-link>
        <router-link to="/profile" class="nav-link">👤 Профиль</router-link>
      </nav>

      <!-- Правая часть: Действия -->
      <div class="topbar-right">
        <!-- Не авторизован -->
        <template v-if="!authStore.token">
          <router-link to="/login" class="btn btn-outline">
            Войти
          </router-link>
          <router-link to="/register" class="btn btn-primary">
            Регистрация
          </router-link>
        </template>

        <!-- Авторизован -->
        <template v-else>
          <div class="user-menu">
            <button @click="handleLogout" class="btn btn-danger">
              Выйти
            </button>
          </div>
        </template>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const handleLogout = async () => {
  await authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.topbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 64px;
  background: #ffffff;
  border-bottom: 1px solid #e8ecf1;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
  z-index: 1000;
}

.topbar-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

/* Левая часть */
.topbar-left {
  display: flex;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  color: #2c3e50;
  font-weight: 700;
  font-size: 20px;
}

.logo-icon {
  font-size: 24px;
}

.logo-text {
  color: #4a6cf7;
}

/* Навигация */
.topbar-nav {
  display: flex;
  gap: 4px;
  align-items: center;
}

.nav-link {
  color: #4a5568;
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
  padding: 8px 16px;
  border-radius: 8px;
  transition: all 0.2s;
}

.nav-link:hover {
  background: #f0f4ff;
  color: #4a6cf7;
}

.nav-link.router-link-active {
  color: #4a6cf7;
  background: #f0f4ff;
}

/* Правая часть */
.topbar-right {
  display: flex;
  gap: 12px;
  align-items: center;
}

/* Кнопки */
.btn {
  padding: 8px 20px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.btn-outline {
  background: transparent;
  border: 1.5px solid #4a6cf7;
  color: #4a6cf7;
}

.btn-outline:hover {
  background: #4a6cf7;
  color: white;
}

.btn-primary {
  background: #4a6cf7;
  color: white;
}

.btn-primary:hover {
  background: #3b5de7;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(74, 108, 247, 0.3);
}

.btn-danger {
  background: #ef4444;
  color: white;
  padding: 8px 16px;
}

.btn-danger:hover {
  background: #dc2626;
}

/* Меню пользователя */
.user-menu {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-email {
  color: #2c3e50;
  font-size: 14px;
  font-weight: 500;
}

/* Адаптивность */
@media (max-width: 768px) {
  .topbar-nav {
    display: none;
  }

  .logo-text {
    display: none;
  }

  .btn {
    padding: 6px 14px;
    font-size: 13px;
  }

  .user-email {
    display: none;
  }
}
</style>

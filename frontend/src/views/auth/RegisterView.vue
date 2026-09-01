<template>
  <div class="auth-page">
    <div class="auth-card">
      <h2>📝 Регистрация</h2>

      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label>Имя пользователя</label>
          <input
            v-model="username"
            type="text"
            placeholder="john_doe"
            required
            minlength="3"
          />
        </div>

        <div class="form-group">
          <label>Email</label>
          <input
            v-model="email"
            type="email"
            placeholder="user@example.com"
            required
          />
        </div>

        <div class="form-group">
          <label>Пароль</label>
          <input
            v-model="password"
            type="password"
            placeholder="••••••••"
            required
            minlength="6"
          />
        </div>

        <button type="submit" class="btn-submit" :disabled="authStore.loading">
          {{ authStore.loading ? 'Загрузка...' : 'Зарегистрироваться' }}
        </button>

        <p v-if="authStore.error" class="error">{{ authStore.error }}</p>

        <p class="auth-link">
          Уже есть аккаунт? <router-link to="/login">Войти</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const username = ref('')
const email = ref('')
const password = ref('')

const handleRegister = async () => {
  const result = await authStore.register({
    username: username.value,
    email: email.value,
    password: password.value
  })

  if (result.success) {
    // После регистрации перенаправляем на страницу входа
    router.push('/login')
  }
}
</script>

<style scoped>
/* Стили такие же как в LoginView */
.auth-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 70vh;
}

.auth-card {
  background: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
  width: 100%;
  max-width: 400px;
}

.auth-card h2 {
  margin-bottom: 24px;
  color: #2c3e50;
  text-align: center;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-weight: 500;
  color: #4a5568;
  font-size: 14px;
}

.form-group input {
  width: 100%;
  padding: 10px 14px;
  border: 1.5px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  transition: all 0.2s;
}

.form-group input:focus {
  outline: none;
  border-color: #4a6cf7;
  box-shadow: 0 0 0 3px rgba(74, 108, 247, 0.1);
}

.btn-submit {
  width: 100%;
  padding: 12px;
  background: #4a6cf7;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 8px;
}

.btn-submit:hover:not(:disabled) {
  background: #3b5de7;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(74, 108, 247, 0.3);
}

.btn-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error {
  color: #ef4444;
  font-size: 14px;
  margin-top: 12px;
  text-align: center;
}

.auth-link {
  margin-top: 16px;
  text-align: center;
  color: #4a5568;
  font-size: 14px;
}

.auth-link a {
  color: #4a6cf7;
  text-decoration: none;
  font-weight: 500;
}

.auth-link a:hover {
  text-decoration: underline;
}
</style>

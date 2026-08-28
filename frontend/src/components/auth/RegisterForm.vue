<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Создать аккаунт
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          Уже есть аккаунт?
          <router-link to="/login" class="font-medium text-indigo-600 hover:text-indigo-500">
            Войти
          </router-link>
        </p>
      </div>

      <form class="mt-8 space-y-6" @submit.prevent="handleRegister">
        <div class="rounded-md shadow-sm space-y-4">
          <!-- Username -->
          <div>
            <label for="username" class="sr-only">Имя пользователя</label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              required
              class="appearance-none rounded-lg relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
              placeholder="Имя пользователя"
              :disabled="loading"
            />
          </div>

          <!-- Email -->
          <div>
            <label for="email" class="sr-only">Email</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              required
              class="appearance-none rounded-lg relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
              placeholder="Email"
              :disabled="loading"
            />
          </div>

          <!-- Password -->
          <div>
            <label for="password" class="sr-only">Пароль</label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              required
              minlength="6"
              class="appearance-none rounded-lg relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
              placeholder="Пароль (минимум 6 символов)"
              :disabled="loading"
            />
          </div>

          <!-- Confirm Password -->
          <div>
            <label for="confirmPassword" class="sr-only">Подтвердите пароль</label>
            <input
              id="confirmPassword"
              v-model="form.confirmPassword"
              type="password"
              required
              class="appearance-none rounded-lg relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm"
              placeholder="Подтвердите пароль"
              :disabled="loading"
            />
          </div>
        </div>

        <!-- Ошибки -->
        <div v-if="error" class="text-red-600 text-sm text-center">
          {{ error }}
        </div>

        <div v-if="successMessage" class="text-green-600 text-sm text-center">
          {{ successMessage }}
        </div>

        <!-- Submit -->
        <div>
          <button
            type="submit"
            :disabled="loading || !isFormValid"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="loading" class="flex items-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Регистрация...
            </span>
            <span v-else>Зарегистрироваться</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const router = useRouter()
const authStore = useAuthStore()

const form = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
})

const loading = computed(() => authStore.loading)
const error = ref(null)
const successMessage = ref(null)

const isFormValid = computed(() => {
  return (
    form.value.username.length >= 3 &&
    form.value.email.includes('@') &&
    form.value.password.length >= 6 &&
    form.value.password === form.value.confirmPassword
  )
})

const handleRegister = async () => {
  error.value = null
  successMessage.value = null

  if (!isFormValid.value) {
    error.value = 'Пожалуйста, заполните все поля корректно'
    return
  }

  const result = await authStore.register({
    username: form.value.username,
    email: form.value.email,
    password: form.value.password,
  })

  if (result.success) {
    successMessage.value = 'Регистрация успешна! Перенаправление на страницу входа...'
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } else {
    error.value = result.error
  }
}
</script>

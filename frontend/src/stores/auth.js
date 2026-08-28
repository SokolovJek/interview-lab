import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authAPI } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || null)
  const loading = ref(false)
  const error = ref(null)

  const register = async (userData) => {
    loading.value = true
    error.value = null
    try {
      const response = await authAPI.register(userData)
      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.detail || 'Ошибка регистрации'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const login = async (credentials) => {
    loading.value = true
    error.value = null
    try {
      const response = await authAPI.login(credentials)
      token.value = response.data.access_token
      localStorage.setItem('token', token.value)

      // Получаем информацию о пользователе
      try {
        const userResponse = await authAPI.getCurrentUser(token.value)
        user.value = userResponse.data
      } catch (e) {
        // Если не удалось получить пользователя, используем email из запроса
        user.value = { email: credentials.username }
      }

      return { success: true, data: response.data }
    } catch (err) {
      error.value = err.response?.data?.detail || 'Ошибка входа'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const logout = async () => {
    try {
      if (token.value) {
        await authAPI.logout(token.value)
      }
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      token.value = null
      user.value = null
      localStorage.removeItem('token')
    }
  }

  // Получение текущего пользователя
  const getCurrentUser = async () => {
    if (!token.value) return null
    try {
      const response = await authAPI.getCurrentUser(token.value)
      user.value = response.data
      return response.data
    } catch (err) {
      console.error('Get current user error:', err)
      return null
    }
  }

  return {
    user,
    token,
    loading,
    error,
    register,
    login,
    logout,
    getCurrentUser,
  }
})

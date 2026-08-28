import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const authAPI = {
  // Регистрация
  register: (userData) => {
    return api.post('/users/register', userData)
  },

  // Логин (OAuth2)
  login: (credentials) => {
    // OAuth2 ожидает form-data
    const formData = new URLSearchParams()
    formData.append('username', credentials.username)
    formData.append('password', credentials.password)

    return api.post('/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
  },

  // Logout
  logout: (token) => {
    return api.post('/logout', null, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
  },

  // Получить текущего пользователя
  getCurrentUser: (token) => {
    return api.get('/users/', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
  },
}

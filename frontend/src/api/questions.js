import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Добавляем интерсептор для автоматической установки токена
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

export const questionsAPI = {
  // Получение статистики пользователя
  getMyStats: () => api.get('/questions/my/stats'),

  // Получение вопросов пользователя с фильтром по статусу
  getMyQuestions: (params) => api.get('/questions/my/questions', { params }),

  // Получение всех вопросов (для админов)
  getAllQuestions: (params) => api.get('/questions', { params }),

  // Получение случайных вопросов
  getRandomQuestions: (limit = 10) => {
    return api.get('/questions/random', { params: { limit: Number(limit) } })
  },

  // Получение вопроса по ID
  getQuestion: (id) => api.get(`/questions/${id}`),

  // Создание вопроса (только для админов)
  createQuestion: (data) => api.post('/questions', data),

  // Обновление вопроса (только для админов)
  updateQuestion: (id, data) => api.put(`/questions/${id}`, data),

  // Удаление вопроса (только для админов)
  deleteQuestion: (id) => api.delete(`/questions/${id}`),

  // Обновление статуса вопроса пользователя
  updateQuestionStatus: (data) => api.post('/questions/status', data),
}

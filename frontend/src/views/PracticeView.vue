<template>
  <div class="practice-page">
    <div class="practice-header">
      <h1>🎯 Практика</h1>
      <p class="subtitle">Случайные вопросы для проверки знаний</p>
    </div>

    <!-- Настройки -->
    <div class="practice-settings" v-if="!isPracticing && !showResults">
      <div class="settings-card">
        <h3>⚙️ Настройки</h3>
        <div class="settings-group">
          <label>Количество вопросов</label>
          <select v-model="settings.limit">
            <option value="5">5 вопросов</option>
            <option value="10">10 вопросов</option>
            <option value="15">15 вопросов</option>
            <option value="20">20 вопросов</option>
          </select>
        </div>
        <button class="btn-start" @click="startPractice" :disabled="loading">
          {{ loading ? 'Загрузка...' : 'Начать практику' }}
        </button>
      </div>
    </div>

    <!-- Загрузка -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Загрузка вопросов...</p>
    </div>

    <!-- Ошибка -->
    <div v-if="error" class="error-state">
      <p>❌ {{ error }}</p>
      <button class="btn-retry" @click="startPractice">Повторить</button>
    </div>

    <!-- Нет вопросов -->
    <div v-if="!loading && !error && questions.length === 0 && !showResults && !isPracticing" class="empty-state">
      <p>😕 Нет доступных вопросов</p>
      <p class="empty-hint">Попробуйте позже или добавьте новые вопросы</p>
    </div>

    <!-- Режим практики -->
    <div v-if="isPracticing && currentQuestion" class="practice-mode">
      <!-- Прогресс -->
      <div class="progress-bar">
        <div class="progress-info">
          <span>Вопрос {{ currentIndex + 1 }} из {{ questions.length }}</span>
          <span>{{ progressPercent }}%</span>
        </div>
        <div class="progress-track">
          <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
        </div>
      </div>

      <!-- Карточка вопроса -->
      <div class="question-card">
        <div class="question-number">
          <span class="badge">Вопрос {{ currentIndex + 1 }}</span>
        </div>

        <h3 class="question-title">{{ currentQuestion.id }}: {{ currentQuestion.question || currentQuestion.title }}</h3>

        <!-- Скрытый ответ (показывается только при showAnswer) -->
        <div v-if="showAnswer && currentQuestion.answer" class="answer-section">
          <div class="answer-label">📝 Ответ:</div>
          <div class="answer-content" v-html="renderMarkdown(currentQuestion.answer)"></div>
        </div>

        <!-- Кнопка "Показать ответ" -->
        <div v-if="!showAnswer" class="question-actions">
          <button class="btn-show-answer" @click="showAnswer = true">
            👀 Показать ответ
          </button>
        </div>

        <!-- Действия после показа ответа -->
        <div v-else class="question-actions">
          <!-- Кнопки статуса -->
          <div class="status-buttons">
            <button
              class="btn-status passed"
              @click="updateStatus('passed')"
              :disabled="statusUpdating"
            >
              ✅ Знаю
            </button>
            <button
              class="btn-status repeat"
              @click="updateStatus('repeat')"
              :disabled="statusUpdating"
            >
              🔄 Повторить
            </button>
            <button
              class="btn-status not-passed"
              @click="updateStatus('not_passed')"
              :disabled="statusUpdating"
            >
              ❌ Не знаю
            </button>
          </div>

          <!-- Кнопка "Следующий вопрос" -->
          <button
            class="btn-next"
            @click="nextQuestion"
            :disabled="statusUpdating"
          >
            {{ isLastQuestion ? '📊 Завершить' : '➡️ Следующий' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Результаты -->
    <div v-if="showResults" class="results-card">
      <h2>📊 Результаты практики</h2>

      <div class="results-stats">
        <div class="result-item">
          <span class="result-value">{{ questions.length }}</span>
          <span class="result-label">Всего вопросов</span>
        </div>
        <div class="result-item viewed">
          <span class="result-value">{{ viewedCount }}</span>
          <span class="result-label">Просмотрено</span>
        </div>
        <div class="result-item passed">
          <span class="result-value">{{ statusStats.passed }}</span>
          <span class="result-label">✅ Знаю</span>
        </div>
        <div class="result-item repeat">
          <span class="result-value">{{ statusStats.repeat }}</span>
          <span class="result-label">🔄 Повторить</span>
        </div>
        <div class="result-item not-passed">
          <span class="result-value">{{ statusStats.not_passed }}</span>
          <span class="result-label">❌ Не знаю</span>
        </div>
        <div class="result-item rate">
          <span class="result-value">{{ completionRate }}%</span>
          <span class="result-label">Завершено</span>
        </div>
      </div>

      <div class="results-actions">
        <button class="btn-retry-practice" @click="resetPractice">
          🔄 Начать заново
        </button>
        <router-link to="/dashboard" class="btn-back">
          📊 На дашборд
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import { marked } from 'marked'
import { questionsAPI } from '@/api/questions'

// Настройка marked
marked.setOptions({
  breaks: true,
  gfm: true,
  headerIds: false,
  mangle: false,
})

// Состояния
const loading = ref(false)
const error = ref(null)
const questions = ref([])
const currentIndex = ref(0)
const showAnswer = ref(false)
const isPracticing = ref(false)
const showResults = ref(false)
const viewedQuestions = ref(new Set())
const statusUpdating = ref(false)

// Статистика статусов
const statusStats = reactive({
  passed: 0,
  repeat: 0,
  not_passed: 0,
})

// Настройки
const settings = ref({
  limit: 10,
})

// Вычисляемые свойства
const currentQuestion = computed(() => {
  return questions.value[currentIndex.value] || null
})

const isLastQuestion = computed(() => {
  return questions.value.length > 0 && currentIndex.value === questions.value.length - 1
})

const progressPercent = computed(() => {
  if (questions.value.length === 0) return 0
  return Math.round(((currentIndex.value + 1) / questions.value.length) * 100)
})

const viewedCount = computed(() => {
  return viewedQuestions.value.size
})

const completionRate = computed(() => {
  if (questions.value.length === 0) return 0
  return Math.round((viewedQuestions.value.size / questions.value.length) * 100)
})

// Рендеринг Markdown
const renderMarkdown = (content) => {
  if (!content) return ''
  try {
    return marked.parse(content)
  } catch (error) {
    console.error('Error parsing markdown:', error)
    return content
  }
}

// Методы
const startPractice = async () => {
  loading.value = true
  error.value = null
  showResults.value = false
  isPracticing.value = false
  currentIndex.value = 0
  showAnswer.value = false
  viewedQuestions.value = new Set()
  statusStats.passed = 0
  statusStats.repeat = 0
  statusStats.not_passed = 0

  try {
    const response = await questionsAPI.getRandomQuestions(settings.value.limit)
    questions.value = response.data || []

    if (questions.value.length === 0) {
      error.value = 'Нет доступных вопросов'
    } else {
      isPracticing.value = true
    }
  } catch (err) {
    console.error('Error starting practice:', err)
    error.value = err.response?.data?.detail || 'Не удалось загрузить вопросы'
  } finally {
    loading.value = false
  }
}

const updateStatus = async (status) => {
  if (!currentQuestion.value) return

  statusUpdating.value = true

  try {
    await questionsAPI.updateQuestionStatus({
      question_id: currentQuestion.value.id,
      status: status
    })

    // Обновляем статистику
    statusStats[status] = (statusStats[status] || 0) + 1

    // Отмечаем вопрос как просмотренный
    viewedQuestions.value.add(currentQuestion.value.id)

    // Если это последний вопрос - завершаем
    if (isLastQuestion.value) {
      isPracticing.value = false
      showResults.value = true
    } else {
      // Переход к следующему вопросу
      currentIndex.value++
      showAnswer.value = false
    }
  } catch (err) {
    console.error('Error updating status:', err)
    error.value = 'Не удалось обновить статус вопроса'
  } finally {
    statusUpdating.value = false
  }
}

const nextQuestion = () => {
  // Если ответ не показан - показываем
  if (!showAnswer.value) {
    showAnswer.value = true
    return
  }

  // Если ответ показан - переходим к следующему вопросу
  // Отмечаем текущий вопрос как просмотренный
  if (currentQuestion.value) {
    viewedQuestions.value.add(currentQuestion.value.id)
  }

  if (isLastQuestion.value) {
    // Завершаем практику
    isPracticing.value = false
    showResults.value = true
  } else {
    // Следующий вопрос
    currentIndex.value++
    showAnswer.value = false
  }
}

const resetPractice = () => {
  showResults.value = false
  questions.value = []
  currentIndex.value = 0
  showAnswer.value = false
  viewedQuestions.value = new Set()
  isPracticing.value = false
  statusStats.passed = 0
  statusStats.repeat = 0
  statusStats.not_passed = 0
  startPractice()
}
</script>

<style scoped>
.practice-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 16px;
}

.practice-header {
  margin-bottom: 32px;
}

.practice-header h1 {
  font-size: 32px;
  color: #2c3e50;
  margin-bottom: 8px;
}

.practice-header .subtitle {
  color: #6b7a8f;
  font-size: 16px;
}

/* Настройки */
.practice-settings {
  margin-bottom: 32px;
}

.settings-card {
  background: white;
  padding: 32px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.settings-card h3 {
  margin: 0 0 20px 0;
  color: #2c3e50;
}

.settings-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
}

.settings-group label {
  font-size: 14px;
  font-weight: 500;
  color: #4a5568;
}

.settings-group select {
  padding: 10px 14px;
  border: 1.5px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  background: white;
  cursor: pointer;
}

.settings-group select:focus {
  outline: none;
  border-color: #4a6cf7;
}

.btn-start {
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
}

.btn-start:hover:not(:disabled) {
  background: #3b5de7;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(74, 108, 247, 0.3);
}

.btn-start:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Загрузка */
.loading-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 12px;
}

.loading-state .spinner {
  width: 48px;
  height: 48px;
  border: 4px solid #e2e8f0;
  border-top: 4px solid #4a6cf7;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 16px;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Ошибка */
.error-state {
  text-align: center;
  padding: 40px 20px;
  background: #fff5f5;
  border-radius: 12px;
  border: 1px solid #fed7d7;
}

.error-state p {
  color: #e53e3e;
  margin-bottom: 16px;
}

.btn-retry {
  padding: 8px 24px;
  background: #4a6cf7;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}

/* Пустое состояние */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 12px;
}

.empty-state p {
  color: #6b7a8f;
}

.empty-hint {
  font-size: 14px;
  color: #a0aec0;
}

/* Прогресс */
.progress-bar {
  margin-bottom: 24px;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  font-size: 14px;
  color: #4a5568;
  margin-bottom: 8px;
}

.progress-track {
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: #4a6cf7;
  transition: width 0.3s ease;
  border-radius: 4px;
}

/* Карточка вопроса */
.question-card {
  background: white;
  padding: 32px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.question-number {
  margin-bottom: 16px;
}

.badge {
  display: inline-block;
  padding: 4px 12px;
  background: #e2e8f0;
  border-radius: 20px;
  font-size: 13px;
  color: #4a5568;
}

.question-title {
  font-size: 20px;
  color: #2c3e50;
  margin: 0 0 20px 0;
  line-height: 1.5;
}

/* Секция ответа */
.answer-section {
  background: #f0f4ff;
  padding: 16px 20px;
  border-radius: 8px;
  border-left: 4px solid #4a6cf7;
  margin-bottom: 24px;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.answer-label {
  font-size: 13px;
  font-weight: 600;
  color: #4a6cf7;
  margin-bottom: 4px;
}

.answer-text {
  font-size: 16px;
  color: #2c3e50;
}

/* Кнопки */
.question-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.btn-show-answer {
  padding: 12px 24px;
  background: #4a6cf7;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  width: 100%;
}

.btn-show-answer:hover {
  background: #3b5de7;
  transform: translateY(-1px);
}

/* Кнопки статуса */
.status-buttons {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.btn-status {
  padding: 12px 16px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-status:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.btn-status:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-status.passed {
  background: #48bb78;
  color: white;
}

.btn-status.passed:hover:not(:disabled) {
  background: #38a169;
}

.btn-status.repeat {
  background: #ed8936;
  color: white;
}

.btn-status.repeat:hover:not(:disabled) {
  background: #dd6b20;
}

.btn-status.not-passed {
  background: #fc8181;
  color: white;
}

.btn-status.not-passed:hover:not(:disabled) {
  background: #e53e3e;
}

/* Кнопка следующий */
.btn-next {
  padding: 12px 24px;
  background: #4a6cf7;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  width: 100%;
}

.btn-next:hover:not(:disabled) {
  background: #3b5de7;
  transform: translateY(-1px);
}

.btn-next:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Результаты */
.results-card {
  background: white;
  padding: 32px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.results-card h2 {
  text-align: center;
  margin-bottom: 24px;
  color: #2c3e50;
}

.results-stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.result-item {
  text-align: center;
  padding: 16px;
  border-radius: 8px;
  background: #f8fafc;
}

.result-item .result-value {
  display: block;
  font-size: 28px;
  font-weight: 700;
  color: #2c3e50;
}

.result-item .result-label {
  font-size: 14px;
  color: #6b7a8f;
}

.result-item.viewed .result-value {
  color: #4a6cf7;
}

.result-item.passed .result-value {
  color: #48bb78;
}

.result-item.repeat .result-value {
  color: #ed8936;
}

.result-item.not-passed .result-value {
  color: #fc8181;
}

.result-item.rate .result-value {
  color: #4a6cf7;
}

.results-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.btn-retry-practice,
.btn-back {
  padding: 10px 24px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.2s;
}

.btn-retry-practice {
  background: #4a6cf7;
  color: white;
  border: none;
}

.btn-retry-practice:hover {
  background: #3b5de7;
}

.btn-back {
  background: #e2e8f0;
  color: #4a5568;
  border: none;
}

.btn-back:hover {
  background: #cbd5e0;
}

@media (max-width: 768px) {
  .status-buttons {
    grid-template-columns: 1fr;
  }

  .results-stats {
    grid-template-columns: repeat(2, 1fr);
  }

  .results-actions {
    flex-direction: column;
  }

  .btn-retry-practice,
  .btn-back {
    width: 100%;
    text-align: center;
  }
  .question-content :deep(pre) {
    background: #1a1a2e;
    color: #e2e8f0;
    padding: 16px;
    border-radius: 8px;
    overflow-x: auto;
    margin: 12px 0;
    font-family: 'Fira Code', 'Courier New', monospace;
    font-size: 14px;
    line-height: 1.6;
  }

  .question-content :deep(code) {
    background: #edf2f7;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'Fira Code', 'Courier New', monospace;
    font-size: 14px;
    color: #2d3748;
  }

  .question-content :deep(pre code) {
    background: transparent;
    padding: 0;
    color: inherit;
  }

  .question-content :deep(h1),
  .question-content :deep(h2),
  .question-content :deep(h3),
  .question-content :deep(h4) {
    margin: 16px 0 8px 0;
    color: #2c3e50;
  }

  .question-content :deep(p) {
    margin: 8px 0;
    line-height: 1.6;
  }

  .question-content :deep(ul),
  .question-content :deep(ol) {
    margin: 8px 0 8px 20px;
  }

  .question-content :deep(blockquote) {
    border-left: 4px solid #4a6cf7;
    padding-left: 16px;
    margin: 12px 0;
    color: #4a5568;
  }

  .question-content :deep(table) {
    border-collapse: collapse;
    width: 100%;
    margin: 12px 0;
  }

  .question-content :deep(th),
  .question-content :deep(td) {
    border: 1px solid #e2e8f0;
    padding: 8px 12px;
    text-align: left;
  }

  .question-content :deep(th) {
    background: #f7fafc;
    font-weight: 600;
  }

  .question-content :deep(a) {
    color: #4a6cf7;
    text-decoration: none;
  }

  .question-content :deep(a:hover) {
    text-decoration: underline;
  }

  /* Стили для ответа с Markdown */
  .answer-content :deep(pre) {
    background: #1a1a2e;
    color: #e2e8f0;
    padding: 16px;
    border-radius: 8px;
    overflow-x: auto;
    margin: 12px 0;
    font-family: 'Fira Code', 'Courier New', monospace;
    font-size: 14px;
    line-height: 1.6;
  }

  .answer-content :deep(code) {
    background: #edf2f7;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'Fira Code', 'Courier New', monospace;
    font-size: 14px;
    color: #2d3748;
  }

  .answer-content :deep(pre code) {
    background: transparent;
    padding: 0;
    color: inherit;
  }

  .answer-content :deep(p) {
    margin: 8px 0;
    line-height: 1.6;
  }

  .answer-content :deep(ul),
  .answer-content :deep(ol) {
    margin: 8px 0 8px 20px;
  }

  .answer-content :deep(blockquote) {
    border-left: 4px solid #4a6cf7;
    padding-left: 16px;
    margin: 12px 0;
    color: #4a5568;
  }

  .answer-content :deep(table) {
    border-collapse: collapse;
    width: 100%;
    margin: 12px 0;
  }

  .answer-content :deep(th),
  .answer-content :deep(td) {
    border: 1px solid #e2e8f0;
    padding: 8px 12px;
    text-align: left;
  }

  .answer-content :deep(th) {
    background: #f7fafc;
    font-weight: 600;
  }

  .answer-content :deep(a) {
    color: #4a6cf7;
    text-decoration: none;
  }

  .answer-content :deep(a:hover) {
    text-decoration: underline;
  }
}

</style>

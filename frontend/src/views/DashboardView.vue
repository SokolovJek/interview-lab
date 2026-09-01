<template>
  <div class="dashboard-page">
    <div class="dashboard-header">
      <h1>📊 Дашборд</h1>
      <p class="subtitle">Добро пожаловать в систему управления вопросами</p>
    </div>

    <!-- Статистика -->
    <div class="stats-grid">
      <div class="stat-card" v-if="!loadingStats">
        <div class="stat-icon">📝</div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.total_questions || 0 }}</span>
          <span class="stat-label">Всего вопросов</span>
        </div>
      </div>
      <div class="stat-card" v-if="!loadingStats">
        <div class="stat-icon">✅</div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.passed || 0 }}</span>
          <span class="stat-label">Пройдено</span>
        </div>
      </div>
      <div class="stat-card" v-if="!loadingStats">
        <div class="stat-icon">🔄</div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.repeat || 0 }}</span>
          <span class="stat-label">На повторение</span>
        </div>
      </div>
      <div class="stat-card" v-if="!loadingStats">
        <div class="stat-icon">⏳</div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.in_progress || 0 }}</span>
          <span class="stat-label">В процессе</span>
        </div>
      </div>
      <div class="stat-card" v-if="!loadingStats">
        <div class="stat-icon">❌</div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.not_passed || 0 }}</span>
          <span class="stat-label">Не пройдено</span>
        </div>
      </div>
      <div class="stat-card" v-if="!loadingStats">
        <div class="stat-icon">📈</div>
        <div class="stat-info">
          <span class="stat-value">{{ stats.success_rate || 0 }}%</span>
          <span class="stat-label">Успеваемость</span>
        </div>
      </div>
    </div>

    <!-- Загрузка статистики -->
    <div v-if="loadingStats" class="loading-state">
      <div class="spinner"></div>
      <p>Загрузка статистики...</p>
    </div>

    <!-- Ошибка загрузки -->
    <div v-if="error" class="error-state">
      <p>❌ {{ error }}</p>
      <button class="btn-retry" @click="loadStats">Повторить</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { questionsAPI } from '@/api/questions'

// Состояния
const loadingStats = ref(false)
const error = ref(null)
const stats = ref({
  total_questions: 0,
  passed: 0,
  repeat: 0,
  in_progress: 0,
  not_passed: 0,
  success_rate: 0,
})

// Методы
const loadStats = async () => {
  loadingStats.value = true
  error.value = null

  try {
    const response = await questionsAPI.getMyStats()
    stats.value = response.data
  } catch (err) {
    console.error('Error loading stats:', err)
    error.value = err.response?.data?.detail || 'Не удалось загрузить статистику'
  } finally {
    loadingStats.value = false
  }
}

// Автоматическая загрузка при монтировании
onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.dashboard-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px;
}

.dashboard-header {
  margin-bottom: 32px;
}

.dashboard-header h1 {
  font-size: 32px;
  color: #2c3e50;
  margin-bottom: 8px;
}

.dashboard-header .subtitle {
  color: #6b7a8f;
  font-size: 16px;
}

/* Статистика */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: all 0.2s;
  border: 1px solid #f0f0f0;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  font-size: 32px;
  line-height: 1;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: #2c3e50;
}

.stat-label {
  font-size: 14px;
  color: #6b7a8f;
}

/* Загрузка */
.loading-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
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

.loading-state p {
  color: #6b7a8f;
  font-size: 16px;
}

/* Ошибка */
.error-state {
  text-align: center;
  padding: 40px 20px;
  background: #fff5f5;
  border-radius: 12px;
  border: 1px solid #fed7d7;
  margin-bottom: 32px;
}

.error-state p {
  color: #e53e3e;
  font-size: 16px;
  margin-bottom: 16px;
}

.btn-retry {
  padding: 8px 24px;
  background: #4a6cf7;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-retry:hover {
  background: #3b5de7;
  transform: translateY(-1px);
}

/* Информация о пользователе */
.user-info-card {
  background: white;
  padding: 24px 32px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  margin-bottom: 32px;
  border: 1px solid #f0f0f0;
}

.user-info-card h3 {
  margin: 0 0 16px 0;
  color: #2c3e50;
  font-size: 18px;
}

.user-info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-size: 13px;
  color: #6b7a8f;
  font-weight: 500;
}

.info-value {
  font-size: 16px;
  color: #2c3e50;
  font-weight: 500;
}

.role-badge {
  display: inline-block;
  padding: 2px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
  background: #e2e8f0;
  color: #4a5568;
}

.role-badge.admin {
  background: #fefcbf;
  color: #744210;
}

/* Быстрые действия */
.quick-actions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.action-card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  text-decoration: none;
  color: #2c3e50;
  border: 1px solid #f0f0f0;
  transition: all 0.2s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.action-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  border-color: #4a6cf7;
}

.action-icon {
  font-size: 28px;
  display: block;
  margin-bottom: 8px;
}

.action-card h4 {
  margin: 0 0 4px 0;
  font-size: 16px;
  color: #2c3e50;
}

.action-card p {
  margin: 0;
  font-size: 14px;
  color: #6b7a8f;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .user-info-grid {
    grid-template-columns: 1fr;
  }

  .quick-actions {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }

  .dashboard-header h1 {
    font-size: 24px;
  }
}
</style>

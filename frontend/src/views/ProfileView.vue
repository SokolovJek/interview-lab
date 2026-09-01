<template>
  <div class="profile-page">
    <div class="profile-header">
      <h1>👤 Профиль</h1>
      <p class="subtitle">Управление личными данными</p>
    </div>

    <div class="profile-content">
      <!-- Информация о пользователе -->
      <div class="profile-card">
        <div class="avatar-section">
          <div class="avatar">
            {{ userInitials }}
          </div>
          <h2>{{ authStore.user?.username || 'User' }}</h2>
          <p class="email">{{ authStore.user?.email }}</p>
        </div>

        <div class="info-section">
          <div class="info-item">
            <span class="info-label">Имя пользователя</span>
            <span class="info-value">{{ authStore.user?.username }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">Email</span>
            <span class="info-value">{{ authStore.user?.email }}</span>
          </div>
          <div class="info-item">
            <span class="info-label">Статус</span>
            <span class="info-value">
              <span class="status-badge active">Активен</span>
            </span>
          </div>
          <div class="info-item">
            <span class="info-label">Роль</span>
            <span class="info-value">
              <span class="role-badge" :class="{ admin: authStore.user?.is_superuser }">
                {{ authStore.user?.is_superuser ? 'Администратор' : 'Пользователь' }}
              </span>
            </span>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const updateMessage = ref('')

const editForm = ref({
  username: '',
  email: '',
  password: '',
})

const userInitials = computed(() => {
  const username = authStore.user?.username || 'U'
  return username.charAt(0).toUpperCase()
})

const formatDate = (dateString) => {
  if (!dateString) return '—'
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('ru-RU', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  }).format(date)
}

const resetForm = () => {
  editForm.value = {
    username: authStore.user?.username || '',
    email: authStore.user?.email || '',
    password: '',
  }
  updateMessage.value = ''
}

onMounted(() => {
  resetForm()
})
</script>

<style scoped>
.profile-page {
  max-width: 800px;
  margin: 0 auto;
}

.profile-header {
  margin-bottom: 32px;
}

.profile-header h1 {
  font-size: 32px;
  color: #2c3e50;
  margin-bottom: 8px;
}

.profile-header .subtitle {
  color: #6b7a8f;
  font-size: 16px;
}

.profile-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Карточка профиля */
.profile-card {
  background: white;
  padding: 32px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.avatar-section {
  text-align: center;
  margin-bottom: 24px;
}

.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: #4a6cf7;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  font-weight: 600;
  margin: 0 auto 12px;
}

.avatar-section h2 {
  margin: 0;
  color: #2c3e50;
  font-size: 20px;
}

.avatar-section .email {
  color: #6b7a8f;
  margin: 4px 0 0;
}

.info-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
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
  font-size: 15px;
  color: #2c3e50;
}

.status-badge {
  display: inline-block;
  padding: 2px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 500;
}

.status-badge.active {
  background: #c6f6d5;
  color: #22543d;
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

/* Карточка редактирования */
.edit-card {
  background: white;
  padding: 24px 32px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.edit-card h3 {
  margin: 0 0 20px 0;
  color: #2c3e50;
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

.form-actions {
  display: flex;
  gap: 12px;
  margin-top: 8px;
}

.btn-save {
  padding: 10px 24px;
  background: #4a6cf7;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-save:hover:not(:disabled) {
  background: #3b5de7;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(74, 108, 247, 0.3);
}

.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-reset {
  padding: 10px 24px;
  background: #e2e8f0;
  color: #4a5568;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-reset:hover {
  background: #cbd5e0;
}

.message {
  margin-top: 12px;
  padding: 10px 16px;
  border-radius: 8px;
  font-size: 14px;
}

.message.success {
  background: #c6f6d5;
  color: #22543d;
}

.message.error {
  background: #fed7d7;
  color: #742a2a;
}

/* Карточка действий */
.actions-card {
  background: white;
  padding: 24px 32px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.actions-card h3 {
  margin: 0 0 16px 0;
  color: #2c3e50;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 12px;
}

.action-btn {
  padding: 12px 20px;
  background: #f8fafc;
  border: 1.5px solid #e2e8f0;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  color: #2c3e50;
}

.action-btn:hover {
  background: #f0f4ff;
  border-color: #4a6cf7;
  transform: translateY(-1px);
}

.action-btn.danger:hover {
  background: #fff5f5;
  border-color: #f56565;
  color: #e53e3e;
}

@media (max-width: 768px) {
  .info-section {
    grid-template-columns: 1fr;
  }

  .form-actions {
    flex-direction: column;
  }

  .actions-grid {
    grid-template-columns: 1fr;
  }
}
</style>
<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup>
import { useAuthStore } from './stores/auth'
import { onMounted } from 'vue'

const authStore = useAuthStore()

onMounted(() => {
  // Восстанавливаем сессию при загрузке
  if (authStore.token && !authStore.user) {
    authStore.getCurrentUser()
  }
})
</script>

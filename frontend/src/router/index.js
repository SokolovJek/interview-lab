import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/HomeView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/LoginView.vue'),
    meta: { guest: true },
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/RegisterView.vue'),
    meta: { guest: true },
  },
  {
    path: '/practice',
    name: 'Practice',
    component: () => import('@/views/PracticeView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/DashboardView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/ProfileView.vue'),
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  const token = localStorage.getItem('token')

  // Если есть токен, но нет пользователя - пробуем получить
  if (token && !authStore.user) {
    try {
      await authStore.getCurrentUser()
    } catch (error) {
      authStore.logout()
    }
  }

  const isAuthenticated = !!authStore.user && !!token

  // Проверяем авторизацию
  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
    return
  }

  // Если пользователь авторизован, но пытается зайти на login/register
  if (to.meta.guest && isAuthenticated) {
    next('/')
    return
  }

  next()
})

export default router

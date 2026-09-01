<template>
  <div class="app-layout">
    <TopBar />
    <main class="main-content">
      <slot />
    </main>
    <!-- <FooterBar /> -->
  </div>
</template>

<script setup>
import TopBar from './TopBar.vue'
// import FooterBar from './FooterBar.vue'
</script>

<style scoped>
.app-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  padding: 24px;
  background: #f5f7fa;
  margin-top: 64px; /* Высота топбара */
}
</style>

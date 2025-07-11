<template>
  <div class="admin-layout-wrapper">
    <AdminNavbar />
    <main class="admin-content-area">
      <router-view />
    </main>

    </div>
</template>

<script>
import AdminNavbar from '@/components/AdminNavbar.vue';

export default {
  name: 'AdminLayout',
  components: {
    AdminNavbar,
  },
};
</script>

<style scoped>
.admin-layout-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f8f9fa;
}

.admin-content-area {
  flex-grow: 1;
  width: 100%;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}
</style>
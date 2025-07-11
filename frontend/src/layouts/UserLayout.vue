<template>
  <div class="user-layout-wrapper">
    <UserNavbar />
    <main class="user-content-area">
      <router-view />
    </main>

    </div>
</template>

<script>
import UserNavbar from '@/components/UserNavbar.vue';

export default {
  name: 'UserLayout',
  components: {
    UserNavbar,
  },
};
</script>

<style scoped>
.user-layout-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f8f9fa;
}

.user-content-area {
  flex-grow: 1;
  width: 100%;
  border: none !important;
  outline: none !important;
  box-shadow: none !important;
}
</style>
<template>
  <div
    class="main-bg vh-100 d-flex flex-column justify-content-center align-items-center px-3"
    :style="backgroundStyle"
  >
    <div
      class="card p-5 shadow-lg rounded-4 text-center"
      style="max-width: 400px; width: 100%; background: rgba(255, 255, 255, 0.9);"
    >
      <h1 class="display-5 fw-bold text-pink mb-4">Welcome to ParkPal</h1>
      <p class="mb-4 text-muted fw-medium">
        Choose your role to get started
      </p>

      <div class="d-grid gap-3">
        <button
          class="btn btn-pink fw-semibold btn-lg"
          @click="goToUser"
          aria-label="User login"
        >
          I am a User
        </button>
        <button
          class="btn btn-outline-pink fw-semibold btn-lg"
          @click="goToAdmin"
          aria-label="Admin login"
        >
          I am an Admin
        </button>
      </div>
    </div>

    <footer class="text-center mt-5 text-muted small">
      &copy; {{ new Date().getFullYear() }} ParkPal. All rights reserved.
    </footer>
  </div>
</template>

<script>
import bgImage from '@/assets/background.png'

export default {
  name: 'MainPage',
  computed: {
    backgroundStyle() {
      return {
        backgroundImage: `url(${bgImage})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        backgroundAttachment: 'fixed',
      }
    },
  },
  methods: {
    goToUser() {
      this.$router.push('/user-login') 
    },
    goToAdmin() {
      this.$router.push('/admin-login') 
    },
  },
}
</script>

<style scoped>
.text-pink {
  color: #d63384;
}

.btn-pink {
  background-color: #d63384;
  color: white;
  border-radius: 10px;
  transition: background-color 0.3s ease;
}

.btn-pink:hover {
  background-color: #c2186a;
}

.btn-outline-pink {
  border: 2px solid #d63384;
  color: #d63384;
  border-radius: 10px;
  background-color: transparent;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.btn-outline-pink:hover {
  background-color: #d63384;
  color: white;
  box-shadow: 0 4px 12px rgba(214, 51, 132, 0.3);
}
</style>

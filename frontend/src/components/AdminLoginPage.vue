<template>
  <div
    class="full-bg vh-100 d-flex justify-content-center align-items-start py-5 px-3 overflow-auto"
    :style="backgroundStyle"
  >
    <button class="btn btn-link text-pink fw-semibold back-btn" @click="goHome">
      ← Back to Home
    </button>

    <div
      class="card p-4 shadow-sm"
      style="width: 100%; max-width: 460px; border-radius: 18px;"
    >
      <div class="text-center mb-4">
        <i
          class="bi bi-person-fill-lock icon-pink mb-2"
          style="font-size: 2.8rem;"
        ></i>
        <h4 class="fw-semibold text-dark">Admin Login</h4>
        <p class="text-muted small">Sign in to your admin account</p>
      </div>

      <form @submit.prevent="handleAdminLogin">
        <div class="mb-3">
          <label for="email" class="form-label fw-medium">Username</label>
          <input
            type="text"
            id="email"
            class="form-control"
            placeholder="admin"
            v-model="username"
            required
          />
        </div>

        <div class="mb-3">
          <label for="password" class="form-label fw-medium">Password</label>
          <input
            type="password"
            id="password"
            class="form-control"
            placeholder="Enter password"
            v-model="password"
            required
          />
        </div>

        <button type="submit" class="btn btn-pink w-100 fw-semibold">
          Login
        </button>

        <div v-if="error" class="alert alert-danger mt-3" role="alert">
          {{ error }}
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import bgImage from '@/assets/background.png';
import axios from '@/axios';

export default {
  name: 'AdminLoginPage',
  data() {
    return {
      username: '',
      password: '',
      error: ''
    };
  },
  computed: {
    backgroundStyle() {
      return {
        backgroundImage: `url(${bgImage})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        backgroundAttachment: 'fixed'
      };
    }
  },
  methods: {
    async handleAdminLogin() {
      try {
        const res = await axios.post('/admin-login', {
          username: this.username,
          password: this.password
        }, { withCredentials: true });

        localStorage.setItem('role', res.data.role);
        this.$router.push('/admin/home');
      } catch (err) {
        this.error = err.response?.data?.error || 'Login failed. Please try again.';
      }
    },
    goHome() {
      this.$router.push('/');
    }
  }
};
</script>

<style scoped>
.btn-pink {
  background-color: #d63384;
  color: white;
  border-radius: 10px;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

.btn-pink:hover {
  background-color: #c2186a;
  box-shadow: 0 4px 12px rgba(214, 51, 132, 0.2);
}

.icon-pink {
  color: #d63384;
}

.full-bg {
  overflow-y: auto;
}

.back-btn {
  position: absolute;
  top: 16px;
  left: 16px;
  font-size: 0.9rem;
  padding: 4px 12px;
  color: #d63384 !important;
}
</style>

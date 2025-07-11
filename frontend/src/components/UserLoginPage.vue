<template>
  <div
    class="vh-100 d-flex justify-content-center align-items-center position-relative"
    :style="backgroundStyle"
  >
    <!-- Top-Left Back Button -->
    <button
      class="btn btn-pink back-btn position-absolute"
      @click="goToHome"
    >
      ← Back to Home
    </button>

    <!-- Login Card -->
    <div
      class="card p-4 shadow-sm"
      style="width: 100%; max-width: 420px; border-radius: 18px;"
    >
      <div class="text-center mb-4">
        <i
          class="bi bi-person-circle icon-pink mb-2"
          style="font-size: 2.8rem;"
        ></i>
        <h4 class="fw-semibold text-dark">Welcome Back</h4>
        <p class="text-muted small">Please log in to continue</p>
      </div>

      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label for="email" class="form-label fw-medium">Email address</label>
          <input
            type="email"
            class="form-control"
            id="email"
            placeholder="you@example.com"
            v-model="email"
            required
          />
        </div>

        <div class="mb-3">
          <label for="password" class="form-label fw-medium">Password</label>
          <input
            type="password"
            class="form-control"
            id="password"
            placeholder="Enter password"
            v-model="password"
            required
          />
        </div>

        <button type="submit" class="btn btn-pink w-100 fw-semibold">
          Log In
        </button>

        <div v-if="error" class="alert alert-danger mt-3" role="alert">
          {{ error }}
        </div>
      </form>

      <div class="text-center mt-4">
        <small class="text-muted">
          New to the platform?
          <a
            href="#"
            class="text-pink fw-medium text-decoration-none"
            @click.prevent="redirectToSignup"
          >
            Sign up here
          </a>
        </small>
      </div>
    </div>
  </div>
</template>

<script>
import bgImage from '@/assets/background.png';
import axios from '@/axios';

export default {
  name: 'LoginPage',
  data() {
    return {
      email: '',
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
        backgroundRepeat: 'no-repeat'
      };
    }
  },
  methods: {
    async handleLogin() {
      try {
        const res = await axios.post('http://localhost:5000/user-login', {
          email: this.email,
          password: this.password
        }, { withCredentials: true });

        localStorage.setItem('userId', res.data.id);
        localStorage.setItem('role', res.data.role);
        this.$router.push('/user/home'); // <- update if your user dashboard route is different
      } catch (err) {
        this.error = err.response?.data?.error || 'Login failed. Please try again.';
      }
    },
    redirectToSignup() {
      this.$router.push('/user-signup');
    },
    goToHome() {
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

.back-btn {
  top: 20px;
  left: 20px;
  padding: 6px 14px;
  font-size: 0.9rem;
  position: absolute;
  z-index: 999;
}
</style>

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
        <i class="bi bi-person-plus-fill icon-pink mb-2" style="font-size: 2.8rem;"></i>
        <h4 class="fw-semibold text-dark">Create Account</h4>
        <p class="text-muted small">Sign up to get started</p>
      </div>

      <form @submit.prevent="handleSignup">
        <div class="mb-3">
          <label for="fullname" class="form-label fw-medium">Full Name</label>
          <input
            type="text"
            id="fullname"
            class="form-control"
            placeholder="Your full name"
            v-model="fullname"
            required
          />
        </div>

        <div class="mb-3">
          <label for="email" class="form-label fw-medium">Email address</label>
          <input
            type="email"
            id="email"
            class="form-control"
            placeholder="you@example.com"
            v-model="email"
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

        <div class="mb-3">
          <label for="address" class="form-label fw-medium">Address</label>
          <textarea
            id="address"
            class="form-control"
            placeholder="Your address"
            v-model="address"
            rows="2"
            required
          ></textarea>
        </div>

        <div class="mb-3">
          <label for="pincode" class="form-label fw-medium">Pin Code</label>
          <input
            type="text"
            id="pincode"
            class="form-control"
            placeholder="Pin Code"
            v-model="pincode"
            maxlength="6"
            pattern="\d{6}"
            required
          />
          <div class="form-text">6 digit numeric pin code</div>
        </div>

        <button type="submit" class="btn btn-pink w-100 fw-semibold">
          Sign Up
        </button>
      </form>

      <div class="text-center mt-4">
        <small class="text-muted">
          Already have an account?
          <a
            href="#"
            class="text-pink fw-medium text-decoration-none"
            @click.prevent="redirectToLogin"
          >
            Log in here
          </a>
        </small>
      </div>
    </div>
  </div>
</template>

<script>
import bgImage from '@/assets/background.png'
import axios from '@/axios';

export default {
  name: 'SignUpPage',
  data() {
    return {
      fullname: '',
      email: '',
      password: '',
      address: '',
      pincode: '',
    };
  },
  computed: {
    backgroundStyle() {
      return {
        backgroundImage: `url(${bgImage})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundRepeat: 'no-repeat',
        backgroundAttachment: 'fixed',
      };
    },
  },
  methods: {
    async handleSignup() {
      try {
        const payload = {
          full_name: this.fullname,
          email: this.email,
          password: this.password,
          address: this.address,
          pincode: this.pincode,
        };

        await axios.post('/register', payload);
        alert('Registration successful! Please login.');
        this.redirectToLogin();
      } catch (error) {
        console.log(error);
        if (error.response && error.response.data.error) {
          alert(`Error: ${error.response.data.error}`);
        } else {
          alert('Something went wrong. Please try again.');
        }
      }
    },
    redirectToLogin() {
      this.$router.push('/user-login');
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

<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light shadow-sm py-3">
    <div class="container-fluid">
      <router-link to="/" class="navbar-brand d-flex align-items-center">
        <i class="bi bi-person-circle icon-pink me-2" style="font-size: 1.5rem;"></i>
        <span class="fw-bold text-dark">User Dashboard</span>
      </router-link>

      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link to="/user/home" class="nav-link fw-medium text-dark" active-class="active-link">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/user/summary" class="nav-link fw-medium text-dark" active-class="active-link">Summary</router-link>
          </li>
          <li class="nav-item">
            <a class="nav-link fw-medium text-dark" href="#" @click.prevent="handleLogout">Logout</a>
          </li>
        </ul>

        <ul class="navbar-nav ms-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <router-link to="/user/edit-profile" class="nav-link btn btn-outline-pink fw-medium rounded-pill px-3" active-class="active-outline-btn">
              <i class="bi bi-pencil-square me-1"></i>
              Edit Profile
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'UserNavbar',
  methods: {
    handleLogout() {
      localStorage.removeItem('userId');
      localStorage.removeItem('role');
      this.$router.push('/user-login');
    },
  },
};
</script>

<style scoped>
.navbar {
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.navbar-brand .icon-pink {
  color: #d63384;
}

.nav-link {
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: #c2186a !important;
}

.active-link {
  color: #d63384 !important;
  border-bottom: 2px solid #d63384;
  padding-bottom: 0.3rem;
}

.btn-outline-pink {
  color: #d63384;
  border-color: #d63384;
  transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
}

.btn-outline-pink:hover,
.active-outline-btn {
  background-color: #d63384;
  color: white;
  border-color: #d63384;
}
</style>

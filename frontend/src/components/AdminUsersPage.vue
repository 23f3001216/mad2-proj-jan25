<template>
  <div class="container my-5 registered-users-page">
    <!-- Page Heading -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h3 class="fw-bold text-dark">
        <i class="bi bi-people-fill icon-pink me-2"></i> Registered Users
      </h3>
    </div>

    <!-- Users Table -->
    <div v-if="users.length" class="table-responsive card shadow-sm p-3">
      <table class="table table-hover table-borderless align-middle mb-0">
        <thead class="table-light">
          <tr>
            <th scope="col">User ID</th>
            <th scope="col">Email</th>
            <th scope="col">Full Name</th>
            <th scope="col">Address</th>
            <th scope="col">PIN Code</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td class="fw-medium">{{ user.id }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.name }}</td>
            <td>{{ user.address }}</td>
            <td>{{ user.pin }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- No Users Message -->
    <div v-else class="text-center text-muted mt-5">
      No registered users found.
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AdminUsersPage',
  data() {
    return {
      users: [],
    };
  },
  mounted() {
    axios
      .get('/api/users')
      .then((response) => {
        if (Array.isArray(response.data)) {
          this.users = response.data;
        } else {
          console.warn('Unexpected response format:', response);
        }
      })
      .catch((error) => {
        console.error('Failed to fetch users:', error);
      });
  },
};
</script>

<style scoped>
.icon-pink {
  color: #d63384;
}

.table thead th {
  border-bottom: 2px solid #dee2e6;
}

.table tbody tr:hover {
  background-color: #fff0f5;
}

.table td,
.table th {
  vertical-align: middle;
  padding: 12px;
}
</style>

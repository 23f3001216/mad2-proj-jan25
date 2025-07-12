<template>
  <div class="edit-profile-container">
    <div class="card p-4 shadow-sm">
      <h4 class="fw-semibold mb-3 text-center text-dark">Change Admin Password</h4>

      <form @submit.prevent="updatePassword">
        <div class="mb-3">
          <label class="form-label">New Password</label>
          <input type="password" v-model="newPassword" class="form-control" required />
        </div>

        <div class="text-center">
          <button type="submit" class="btn btn-outline-pink">Update Password</button>
        </div>

        <p v-if="success" class="text-success text-center mt-3">Password updated successfully!</p>
        <p v-if="error" class="text-danger text-center mt-3">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "@/axios";

export default {
  name: "EditAdminProfile",
  data() {
    return {
      newPassword: "",
      success: false,
      error: "",
    };
  },
  methods: {
    async updatePassword() {
      if (!this.newPassword.trim()) {
        this.error = "Password cannot be empty";
        this.success = false;
        return;
      }

      try {
        await axios.put(
          "/api/admin/profile",
          { new_password: this.newPassword },
          { withCredentials: true }
        );
        this.success = true;
        this.error = "";
        this.newPassword = "";
      } catch (err) {
        this.error = "Failed to update password";
        this.success = false;
      }
    },
  },
};
</script>

<style scoped>
.edit-profile-container {
  max-width: 500px;
  margin: 2rem auto;
}
.btn-outline-pink {
  color: #d63384;
  border-color: #d63384;
  transition: 0.3s ease;
  border-radius: 20px;
}
.btn-outline-pink:hover {
  background-color: #d63384;
  color: white;
}
</style>

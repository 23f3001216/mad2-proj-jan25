<template>
  <div class="edit-profile-container">
    <div class="card p-4 shadow-sm">
      <h4 class="fw-semibold mb-3 text-center text-dark">Edit Profile</h4>

      <form @submit.prevent="updateProfile">
        <div class="mb-3">
          <label class="form-label">Full Name</label>
          <input type="text" v-model="form.full_name" class="form-control" required />
        </div>

        <div class="mb-3">
          <label class="form-label">Address</label>
          <input type="text" v-model="form.address" class="form-control" required />
        </div>

        <div class="mb-3">
          <label class="form-label">Pincode</label>
          <input type="text" v-model="form.pincode" class="form-control" required />
        </div>

        <div class="mb-3">
          <label class="form-label">New Password (optional)</label>
          <input type="password" v-model="form.new_password" class="form-control" placeholder="Leave blank to keep current password" />
        </div>

        <div class="text-center">
          <button type="submit" class="btn btn-outline-pink">Save Changes</button>
        </div>

        <p v-if="success" class="text-success text-center mt-3">Profile updated successfully!</p>
        <p v-if="error" class="text-danger text-center mt-3">{{ error }}</p>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "@/axios";

export default {
  name: "EditProfilePage",
  data() {
    return {
      form: {
        full_name: "",
        address: "",
        pincode: "",
        new_password: "", // optional password field
      },
      success: false,
      error: "",
    };
  },
  mounted() {
    this.fetchProfile();
  },
  methods: {
    async fetchProfile() {
      try {
        const res = await axios.get("/api/user/profile", { withCredentials: true });
        this.form.full_name = res.data.full_name;
        this.form.address = res.data.address;
        this.form.pincode = res.data.pincode;
      } catch (err) {
        this.error = "Failed to load profile";
      }
    },
    async updateProfile() {
      try {
        const payload = { ...this.form };
        if (!payload.new_password.trim()) {
          delete payload.new_password; // remove empty password from payload
        }

        await axios.put("/api/user/profile", payload, { withCredentials: true });

        this.success = true;
        this.error = "";
        this.form.new_password = ""; // clear the password field
      } catch (err) {
        this.error = "Failed to update profile";
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

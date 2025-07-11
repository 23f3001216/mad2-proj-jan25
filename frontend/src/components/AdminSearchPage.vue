<template>
  <div class="container my-5">
    <!-- Search Bar -->
    <div class="card shadow-sm p-4 mb-4">
      <h4 class="fw-bold mb-3 text-dark">
        <i class="bi bi-search icon-pink me-2"></i> Search Parking
      </h4>
      <div class="row g-2 align-items-center">
        <div class="col-md-3">
          <label class="form-label fw-medium">Search by:</label>
          <select class="form-select" v-model="searchBy">
            <option>Parking spot by location</option>
            <option>User ID</option>
            <option>User Name</option>
          </select>
        </div>
        <div class="col-md-6">
          <label class="form-label fw-medium">Search text:</label>
          <input
            v-model="searchText"
            type="text"
            class="form-control"
            :placeholder="searchBy.includes('User') ? 'Enter user ID or name' : 'Enter parking location'"
          />
        </div>
        <div class="col-md-3">
          <button class="btn btn-pink mt-4 w-100" @click="performSearch">
            <i class="bi bi-search me-1"></i> Search
          </button>
        </div>
      </div>
    </div>

    <!-- Results -->
    <div v-if="resultType === 'parking_lots' && results.length">
      <h5 class="text-muted fw-semibold mb-3">Found Parking Lots:</h5>
      <div class="row g-4">
        <div class="col-md-6" v-for="lot in results" :key="lot.id">
          <div class="card p-3 shadow-sm">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <h5 class="fw-semibold text-dark">{{ lot.name }}</h5>
            </div>
            <p class="mb-1 text-muted">Address: {{ lot.address }}</p>
            <p class="mb-1 text-muted">Pincode: {{ lot.pincode }}</p>
            <p class="mb-3 text-muted">Price/hr: ₹{{ lot.price }}</p>
            <div class="parking-grid">
              <div
                v-for="(slot, index) in lot.spots"
                :key="slot.id"
                :class="['slot', slot.status === 'O' ? 'occupied' : 'available']"
              >
                {{ index + 1 }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="resultType === 'user' && results.length">
      <h5 class="text-muted fw-semibold mb-3">User Details:</h5>
      <div
        class="card p-3 shadow-sm w-50 mb-3"
        v-for="user in results"
        :key="user.id"
      >
        <p><strong>Name:</strong> {{ user.name }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>Address:</strong> {{ user.address }}</p>
        <p><strong>Pincode:</strong> {{ user.pin }}</p>
      </div>
    </div>

    <div v-if="resultType === 'user' && !results.length">
      <p class="text-danger fw-semibold">No user found with the given input.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SearchParkingVisualization',
  data() {
    return {
      searchBy: 'Parking spot by location',
      searchText: '',
      results: [],
      resultType: null,
    };
  },
  methods: {
    performSearch() {
      if (!this.searchText.trim()) return;
      const by = this.searchBy === 'User ID' || this.searchBy === 'User Name' ? 'user' : 'location';

      axios.get('/api/search-parking', {
        params: {
          by,
          text: this.searchText.trim(),
        },
      })
      .then((res) => {
        this.resultType = res.data.type;
        this.results = res.data.data;
      })
      .catch((err) => {
        console.error('Search failed:', err);
      });
    },
  },
};
</script>

<style scoped>
.icon-pink {
  color: #d63384;
}
.btn-pink {
  background-color: #d63384;
  color: white;
  transition: 0.3s;
}
.btn-pink:hover {
  background-color: #c2186a;
}
.parking-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, 32px);
  gap: 6px;
}
.slot {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  text-align: center;
  line-height: 32px;
  font-weight: bold;
  font-size: 0.9rem;
}
.available {
  background-color: #28a745;
  color: white;
}
.occupied {
  background-color: #d63384;
  color: white;
}
</style>

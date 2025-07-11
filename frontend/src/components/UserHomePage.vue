<template>
  <div class="container my-4 user-home">
    <!-- RECENT PARKING HISTORY -->
    <div class="mb-5">
      <h4 class="fw-bold text-dark mb-3">
        <i class="bi bi-clock-history me-2 icon-pink"></i>
        Recent Parking History
      </h4>
      <div class="table-responsive border rounded shadow-sm">
        <table class="table table-hover mb-0">
          <thead class="table-light">
            <tr>
              <th>ID</th>
              <th>Location</th>
              <th>Vehicle Number</th>
              <th>Timestamp</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="entry in reservations" :key="entry.id">
              <td>{{ entry.spotId }}</td>
              <td>{{ entry.location }}</td>
              <td>{{ entry.vehicleNo }}</td>
              <td>{{ entry.timestamp }}</td>
              <td>
                <button v-if="entry.status === 'O'" class="btn btn-outline-pink btn-sm" @click="openReleaseModal(entry)">Release</button>
                <span v-else class="badge bg-secondary">Parked Out</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- SEARCH PARKING -->
    <div class="mb-4 d-flex align-items-center gap-2">
      <label class="form-label fw-medium text-dark mb-0">Search parking @location/pin code:</label>
      <input type="text" class="form-control w-auto" placeholder="Dadar Road" v-model="searchText" />
      <button class="btn btn-outline-pink btn-sm" @click="fetchLots">Search</button>
    </div>

    <!-- PARKING LOTS LISTING -->
    <div>
      <h4 class="fw-bold text-dark mb-3">
        <i class="bi bi-pin-map-fill me-2 icon-pink"></i>
        Parking Lots
      </h4>
      <div class="table-responsive border rounded shadow-sm">
        <table class="table table-hover mb-0">
          <thead class="table-light">
            <tr>
              <th>ID</th>
              <th>Address</th>
              <th>Availability</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="lot in parkingLots" :key="lot.id">
              <td>{{ lot.id }}</td>
              <td>{{ lot.address }}</td>
              <td>{{ lot.spots.filter(s => s.status === 'A').length }}</td>
              <td>
                <button class="btn btn-outline-pink btn-sm rounded-pill" @click="openBookingModal(lot)">Book</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- RELEASE MODAL -->
    <div v-if="showReleaseModal" class="modal-overlay">
      <div class="modal-content card shadow p-4">
        <h5 class="mb-3 text-center fw-bold text-dark">Release Parking Spot</h5>
        <div class="mb-3">
          <label class="form-label">Spot ID</label>
          <input type="text" class="form-control" :value="releaseData.spotId" disabled />
        </div>
        <div class="mb-3">
          <label class="form-label">Vehicle Number</label>
          <input type="text" class="form-control" :value="releaseData.vehicleNo" disabled />
        </div>
        <div class="mb-3">
          <label class="form-label">Parking Time</label>
          <input type="text" class="form-control" :value="releaseData.parkingTime" disabled />
        </div>
        <div class="mb-3">
          <label class="form-label">Releasing Time</label>
          <input type="text" class="form-control" :value="formatISTDateTime(new Date())" disabled />
        </div>
        <div class="mb-3">
          <label class="form-label">Total Cost</label>
          <input type="text" class="form-control" :value="releaseData.totalCost || '₹60'" disabled />
        </div>
        <div class="text-center mt-3">
          <button class="btn btn-pink me-2" @click="confirmRelease">Release</button>
          <button class="btn btn-secondary" @click="closeReleaseModal">Cancel</button>
        </div>
      </div>
    </div>

    <!-- BOOKING MODAL -->
    <div v-if="showBookModal" class="modal-overlay">
      <div class="modal-content card shadow p-4">
        <h5 class="mb-3 text-center fw-bold text-dark">Reserve Parking Spot</h5>
        <div class="mb-3">
          <label class="form-label">Spot ID</label>
          <input type="text" class="form-control" :value="bookingData.spotId" disabled />
        </div>
        <div class="mb-3">
          <label class="form-label">Lot ID</label>
          <input type="text" class="form-control" :value="bookingData.lotId" disabled />
        </div>
        <div class="mb-3">
          <label class="form-label">Vehicle Number</label>
          <input type="text" class="form-control" v-model="bookingData.vehicleNo" placeholder="Enter vehicle number" />
        </div>
        <div class="text-center mt-3">
          <button class="btn btn-pink me-2" @click="confirmBooking">Reserve</button>
          <button class="btn btn-secondary" @click="closeBookingModal">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '@/axios';
export default {
  name: 'UserHomePage',
  data() {
    return {
      reservations: [],
      parkingLots: [],
      searchText: '',
      showReleaseModal: false,
      showBookModal: false,
      releaseData: {},
      bookingData: {
        spotId: '',
        lotId: '',
        userId: '',
        vehicleNo: '',
      },
    };
  },
  methods: {
    async fetchLots() {
      const res = await axios.get(`/api/user/lots`, {
        params: { search: this.searchText }
      });
      this.parkingLots = res.data;
    },
    async fetchReservations() {
      const res = await axios.get('/api/user/reservations');
      this.reservations = res.data;
    },
    openReleaseModal(entry) {
      this.releaseData = entry;
      this.showReleaseModal = true;
    },
    closeReleaseModal() {
      this.showReleaseModal = false;
    },
    async confirmRelease() {
      await axios.post('/api/user/release', { id: this.releaseData.id });
      this.showReleaseModal = false;
      this.fetchReservations();
      this.fetchLots();
    },
    openBookingModal(lot) {
      const spot = lot.spots.find(s => s.status === 'A');
      if (!spot) return alert('No available spots');
      this.bookingData.spotId = spot.id;
      this.bookingData.lotId = lot.id;
      this.bookingData.vehicleNo = '';
      this.showBookModal = true;
    },
    closeBookingModal() {
      this.showBookModal = false;
    },
    async confirmBooking() {
      if (!this.bookingData.vehicleNo.trim()) {
        alert('Please enter a vehicle number.');
        return;
      }
      await axios.post('/api/user/book', {
        lotId: this.bookingData.lotId,
        vehicleNo: this.bookingData.vehicleNo,
      });
      this.showBookModal = false;
      this.fetchReservations();
      this.fetchLots();
    },
    formatISTDateTime(date) {
      const istOffset = 5.5 * 60 * 60 * 1000;
      const istDate = new Date(date.getTime() + istOffset);

      const pad = (n) => (n < 10 ? '0' + n : n);
      const day = pad(istDate.getDate());
      const month = pad(istDate.getMonth() + 1);
      const year = istDate.getFullYear();

      let hours = istDate.getHours();
      const minutes = pad(istDate.getMinutes());
      const ampm = hours >= 12 ? 'PM' : 'AM';
      hours = hours % 12;
      hours = hours ? hours : 12;

      return `${day}-${month}-${year} ${pad(hours)}:${minutes} ${ampm}`;
    }
  },
  mounted() {
    this.fetchReservations();
    this.fetchLots();
  },
};
</script>

<style scoped>
.icon-pink {
  color: #d63384;
}
.bg-pink {
  background-color: #d63384 !important;
  color: white;
}
.btn-outline-pink {
  color: #d63384;
  border-color: #d63384;
  transition: all 0.3s ease;
}
.btn-outline-pink:hover {
  background-color: #d63384;
  color: white;
}
.btn-pink {
  background-color: #d63384;
  color: white;
  border: none;
  border-radius: 6px;
}
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: 100vw;
  background: rgba(0, 0, 0, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
}
.modal-content {
  background: white;
  border-radius: 16px;
  max-width: 500px;
  width: 100%;
}
</style>

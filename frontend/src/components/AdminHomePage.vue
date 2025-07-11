<template>
  <div class="container my-5 admin-dashboard">
    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h3 class="fw-bold text-dark">
        <i class="bi bi-clipboard-data icon-pink me-2"></i> Admin Dashboard
      </h3>
      <button class="btn btn-outline-pink rounded-pill" @click="openAddPopup">
        <i class="bi bi-plus-circle me-1"></i> Add Parking Lot
      </button>
    </div>

    <!-- Parking Lot Cards -->
    <div class="row g-4">
      <div class="col-md-6" v-for="lot in parkingLots" :key="lot.id">
        <div class="card shadow-sm p-3">
          <!-- Title + Actions -->
          <div class="d-flex justify-content-between align-items-center mb-2">
            <h5 class="fw-semibold text-dark">{{ lot.name }}</h5>
            <div>
              <button class="btn btn-sm btn-outline-secondary me-2" @click="openEditPopup(lot)">
                <i class="bi bi-pencil-square"></i>
              </button>
              <button class="btn btn-sm btn-outline-danger" @click="deleteLot(lot.id)">
                <i class="bi bi-trash"></i>
              </button>
            </div>
          </div>

          <!-- Chart -->
          <div class="chart-wrapper mb-3">
            <Bar :data="getChartData(lot)" :options="chartOptions" />
          </div>

          <!-- Grid Layout -->
          <div class="lot-grid mb-3">
            <div
              v-for="(slot, index) in lot.spots"
              :key="slot.id"
              :class="['parking-slot', slot.status === 'O' ? 'occupied' : 'available']"
            >
              {{ index + 1 }}
              <button
                v-if="slot.status === 'A'"
                @click="deleteSpot(slot.id)"
                class="btn btn-sm btn-danger btn-delete"
              >
                <i class="bi bi-trash-fill"></i>
              </button>
            </div>
          </div>

          <div class="text-center">
            <button class="btn btn-sm btn-outline-pink" @click="addSpot(lot.id)">
              <i class="bi bi-plus-circle"></i> Add Spot
            </button>
          </div>


          <!-- Summary -->
          <p class="text-muted text-center mb-0">
            <strong>{{ lot.spots.filter(s => s.status === 'O').length }}</strong> out of
            <strong>{{ lot.spots.length }}</strong> spots occupied
          </p>
        </div>
      </div>
    </div>

    <!-- Edit/Add Popup Modal -->
    <div v-if="showEditModal" class="modal-backdrop">
      <div class="modal-dialog">
        <div class="modal-content p-4">
          <h5 class="mb-3 fw-bold text-dark">
            {{ isEditMode ? 'Edit Parking Lot Details' : 'Add Parking Lot' }}
          </h5>
          <div class="mb-3">
            <label class="form-label">Name</label>
            <input v-model="editForm.name" type="text" class="form-control" />
          </div>
          <div class="mb-3">
            <label class="form-label">Address</label>
            <input v-model="editForm.address" type="text" class="form-control" />
          </div>
          <div class="mb-3">
            <label class="form-label">Pincode</label>
            <input v-model="editForm.pincode" type="text" class="form-control" />
          </div>
          <div class="mb-3">
            <label class="form-label">Price per Hour</label>
            <input v-model="editForm.price" type="number" class="form-control" />
          </div>
          <div class="mb-3">
            <label class="form-label">Maximum Spots</label>
            <input v-model="editForm.maxSpots" type="number" class="form-control" :disabled="isEditMode" />
          </div>
          <div class="text-end">
            <button class="btn btn-outline-secondary me-2" @click="closeEditPopup">Cancel</button>
            <button class="btn btn-pink" @click="submitForm">{{ isEditMode ? 'Update' : 'Add' }}</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Spot Modal -->
    <div v-if="showSpotModal" class="modal-backdrop">
      <div class="modal-dialog">
        <div class="modal-content p-4">
          <h5 class="mb-3 fw-bold text-dark">Parking Spot Details</h5>
          <p><strong>Spot ID:</strong> {{ selectedSpotIndex + 1 }}</p>
          <p><strong>Status:</strong> {{ selectedSpot.status }}</p>
          <div class="text-end">
            <button class="btn btn-outline-secondary" @click="closeSpotModal">Close</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Bar } from 'vue-chartjs';
import axios from '@/axios';
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
} from 'chart.js';
ChartJS.register(BarElement, CategoryScale, LinearScale, Tooltip, Legend);

export default {
  name: 'AdminDashboardPage',
  components: { Bar },
  data() {
    return {
      parkingLots: [],
      showEditModal: false,
      showSpotModal: false,
      isEditMode: false,
      selectedSpot: {},
      selectedSpotIndex: null,
      selectedLot: null,
      editForm: {
        id: null,
        name: '',
        address: '',
        pincode: '',
        price: '',
        maxSpots: '',
      },
    };
  },
  computed: {
    chartOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: { x: { display: false }, y: { display: false, beginAtZero: true } },
      };
    },
  },
  methods: {
    async fetchLots() {
      const res = await axios.get('/api/parking-lots');
      this.parkingLots = res.data;
    },
    async addSpot(lotId) {
      try {
        await axios.post(`/api/parking-lots/${lotId}/spots`);
        await this.fetchLots();
      } catch (err) {
        alert('Failed to add spot');
      }
    },
    async deleteSpot(spotId) {
      if (confirm('Delete this spot?')) {
        try {
          await axios.delete(`/api/parking-spots/${spotId}`);
          await this.fetchLots();
        } catch (err) {
          alert(err.response?.data?.error || 'Failed to delete');
        }
      }
    },
    async submitForm() {
      try {
        if (this.isEditMode) {
          await axios.put(`/api/parking-lots/${this.editForm.id}`, this.editForm);
        } else {
          await axios.post('/api/parking-lots', this.editForm);
        }
        await this.fetchLots();
        this.closeEditPopup();
      } catch (err) {
        alert('Failed to submit form');
      }
    },
    async deleteLot(id) {
      if (confirm('Are you sure you want to delete this lot?')) {
        try {
          await axios.delete(`/api/parking-lots/${id}`);
          await this.fetchLots();
        } catch (err) {
          alert(err.response?.data?.error || 'Failed to delete');
        }
      }
    },
    openEditPopup(lot) {
      this.editForm = {
        id: lot.id,
        name: lot.name,
        address: lot.address,
        pincode: lot.pincode,
        price: lot.price,
        maxSpots: lot.totalSpots,
      };
      this.isEditMode = true;
      this.showEditModal = true;
    },
    openAddPopup() {
      this.editForm = { id: null, name: '', address: '', pincode: '', price: '', maxSpots: '' };
      this.isEditMode = false;
      this.showEditModal = true;
    },
    closeEditPopup() {
      this.showEditModal = false;
    },
    openSpotDetails(spot, index, lot) {
      this.selectedSpot = spot;
      this.selectedSpotIndex = index;
      this.selectedLot = lot;
      this.showSpotModal = true;
    },
    closeSpotModal() {
      this.showSpotModal = false;
    },
    getChartData(lot) {
      const occupied = lot.spots.filter(s => s.status === 'O').length;
      return {
        labels: ['Occupied', 'Available'],
        datasets: [
          {
            label: 'Spots',
            data: [occupied, lot.spots.length - occupied],
            backgroundColor: ['#d63384', '#f1f1f1'],
            borderRadius: 6,
          },
        ],
      };
    },
  },
  mounted() {
    this.fetchLots();
  },
};
</script>

<style scoped>
.icon-pink {
  color: #d63384;
}

.btn-outline-pink {
  color: #d63384;
  border-color: #d63384;
}

.btn-outline-pink:hover,
.btn-pink {
  background-color: #d63384;
  color: white;
}

.chart-wrapper {
  height: 150px;
}

.lot-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(40px, 1fr));
  gap: 8px;
  padding: 10px;
}

.parking-slot {
  height: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 0.8rem;
  border-radius: 6px;
  color: white;
  font-weight: 600;
  cursor: pointer;
}

.occupied {
  background-color: #d63384;
}

.available {
  background-color: #28a745;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1050;
}

.modal-dialog {
  background: white;
  border-radius: 12px;
  width: 400px;
  max-width: 95%;
}

.btn-delete {
  position: absolute;
  top: 2px;
  right: 2px;
  padding: 0px 4px;
  font-size: 10px;
  border: none;
  border-radius: 50%;
}
.parking-slot {
  position: relative;
}

</style>

<template>
  <div class="summary-page-container">
    <div class="card p-4 shadow-sm">
      <div class="text-center mb-4">
        <i class="bi bi-bar-chart-fill icon-pink mb-2" style="font-size: 2.8rem;"></i>
        <h4 class="fw-semibold text-dark">Your Reservation Summary</h4>
        <p class="text-muted small">Chart showing your completed vs active bookings</p>
      </div>

      <div class="chart-section">
        <div class="chart-wrapper">
          <Doughnut v-if="chartData" :data="chartData" :options="chartOptions" />
        </div>
        <div class="text-center mt-3">
          <p>Total Reservations: <span class="fw-bold">{{ total }}</span></p>
          <p class="text-pink">
            Completed: <strong>{{ completed }}</strong> |
            Active: <strong>{{ active }}</strong>
          </p>
        </div>
      </div>

      <div class="text-center mt-4">
        <button class="btn btn-outline-pink btn-sm" @click="refreshData">
          <i class="bi bi-arrow-clockwise me-1"></i> Refresh
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { Doughnut } from 'vue-chartjs';
import axios from '@/axios';

export default {
  name: 'UserSummaryPage',
  components: { Doughnut },
  data() {
    return {
      completed: 0,
      active: 0,
      chartData: null,
    };
  },
  computed: {
    total() {
      return this.completed + this.active;
    },
    chartOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              usePointStyle: true,
              color: '#333',
              padding: 20,
            },
          },
          tooltip: {
            callbacks: {
              label(context) {
                const total = context.chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
                const value = context.raw;
                const percent = ((value / total) * 100).toFixed(1);
                return `${context.label}: ${value} (${percent}%)`;
              },
            },
          },
        },
      };
    },
  },
  methods: {
    async refreshData() {
      try {
        const res = await axios.get('/api/user/summary', { withCredentials: true });

        this.completed = res.data.completed;
        this.active = res.data.active;

        this.chartData = {
          labels: ['Completed', 'Active'],
          datasets: [
            {
              backgroundColor: ['#d63384', '#ffc107'],
              data: [this.completed, this.active],
              borderRadius: 5,
              hoverOffset: 6,
            },
          ],
        };
      } catch (err) {
        console.error('Failed to fetch user summary:', err);
      }
    },
  },
  mounted() {
    this.refreshData();
  },
};
</script>

<style scoped>
.summary-page-container {
  max-width: 600px;
  margin: 2rem auto;
  padding: 1rem;
}

.card {
  border: none;
  border-radius: 18px;
}

.icon-pink {
  color: #d63384;
}

.text-pink {
  color: #d63384;
}

.chart-wrapper {
  height: 300px;
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
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

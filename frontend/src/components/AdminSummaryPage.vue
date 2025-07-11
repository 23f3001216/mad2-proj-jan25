<template>
  <div class="container my-5 admin-summary-page">
    <!-- Section Heading -->
    <div class="text-center mb-5">
      <h3 class="fw-bold text-dark">
        <i class="bi bi-graph-up-arrow icon-pink me-2"></i>
        Summary shows statistical charts
      </h3>
    </div>

    <!-- Summary Charts -->
    <div class="row g-4">
      <!-- Left: Revenue Chart -->
      <div class="col-md-6">
        <div class="card p-4 shadow-sm chart-card">
          <h5 class="fw-semibold text-center mb-3">Revenue from each parking lot</h5>
          <Doughnut :data="revenueChartData" :options="chartOptions" />
        </div>
      </div>

      <!-- Right: Occupancy Chart -->
      <div class="col-md-6">
        <div class="card p-4 shadow-sm chart-card">
          <h5 class="fw-semibold text-center mb-3">Summary on available and occupied parking lots</h5>
          <Bar :data="occupancyChartData" :options="chartOptions" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement, BarElement, CategoryScale, LinearScale } from 'chart.js';
import { Doughnut, Bar } from 'vue-chartjs';
import axios from 'axios';

ChartJS.register(Title, Tooltip, Legend, ArcElement, BarElement, CategoryScale, LinearScale);

export default {
  name: 'AdminSummaryPage',
  components: { Doughnut, Bar },
  data() {
    return {
      revenueChartData: {
        labels: [],
        datasets: [{
          data: [],
          backgroundColor: ['#d63384', '#f06595', '#fab1c6', '#6f42c1', '#ff6f61'],
        }],
      },
      occupancyChartData: {
        labels: ['Available', 'Occupied', 'Total'],
        datasets: [{
          label: 'Slots',
          data: [0, 0, 0],
          backgroundColor: ['#28a745', '#d63384', '#6c757d'],
        }],
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: {
              usePointStyle: true,
              padding: 15,
            },
          },
        },
      },
    };
  },
  mounted() {
    this.fetchSummary();
  },
  methods: {
    fetchSummary() {
      axios.get('/api/admin/summary').then((res) => {
        const data = res.data;

        // Replace whole objects to ensure reactivity
        this.revenueChartData = {
          labels: data.revenue.map(p => p.name),
          datasets: [{
            data: data.revenue.map(p => p.totalRevenue),
            backgroundColor: ['#d63384', '#f06595', '#fab1c6', '#6f42c1', '#ff6f61'],
          }],
        };

        this.occupancyChartData = {
          labels: ['Available', 'Occupied', 'Total'],
          datasets: [{
            label: 'Slots',
            data: [
              data.occupancy.available,
              data.occupancy.occupied,
              data.occupancy.total,
            ],
            backgroundColor: ['#28a745', '#d63384', '#6c757d'],
          }],
        };
      }).catch((err) => {
        console.error('Error fetching admin summary:', err);
      });
    },
  },
};
</script>

<style scoped>
.icon-pink {
  color: #d63384;
}

.chart-card {
  height: 400px;
  border-radius: 18px;
}

.chart-card canvas {
  max-height: 300px;
}
</style>

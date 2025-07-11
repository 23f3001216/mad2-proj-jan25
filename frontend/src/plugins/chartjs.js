// src/plugins/chartjs.js
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement } from 'chart.js';

// Register all required Chart.js components globally
ChartJS.register(Title, Tooltip, Legend, ArcElement);

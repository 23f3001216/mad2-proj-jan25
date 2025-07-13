import { createApp } from 'vue';
import App from './App.vue';


// Import the router
import router from './router';

// Import Bootstrap CSS
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap';

// Import Bootstrap Icons
import 'bootstrap-icons/font/bootstrap-icons.css';

import './plugins/chartjs';


// Create and mount the Vue app, with the router attached
createApp(App)
    .use(router)
    .mount('#app');
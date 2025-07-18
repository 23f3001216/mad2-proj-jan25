import axios from 'axios';

const instance = axios.create({
    baseURL: 'http://localhost:5000', // Flask backend
    timeout: 5000,
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json'
    }
});

export default instance;

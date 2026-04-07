import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Your laptop's local IPv4 Address pulled natively
// Port 8001 is where the Main Backend runs, Port 8000 is ML Service 
const BASE_URL = 'http://172.20.10.3:8001/api/v1'; 

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor to inject JWT token automatically
api.interceptors.request.use(
  async (config) => {
    const token = await AsyncStorage.getItem('userToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;

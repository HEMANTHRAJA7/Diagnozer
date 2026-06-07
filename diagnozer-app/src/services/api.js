import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// In Expo 49+, environment variables defined in .env prefixed with EXPO_PUBLIC_
// are automatically loaded. Fall back to standard localhost or the active laptop IP.
const DEV_API_URL = 'http://172.20.10.3:8001/api/v1';
const BASE_URL = process.env.EXPO_PUBLIC_API_URL || DEV_API_URL; 

const api = axios.create({
  baseURL: BASE_URL,
  timeout: 300000, // 5 minutes
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

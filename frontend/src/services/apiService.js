import axios from "axios";
import {baseURL} from "../constants/urls";
import {authService} from "./authService";

const apiService = axios.create({baseURL});


apiService.interceptors.request.use(req => {
    const token = localStorage.getItem('access');
    if (token) {
        req.headers.Authorization = `Bearer ${token}`;
    }
    return req;
});


apiService.interceptors.response.use(
    res => res,
    async error => {
        const originalRequest = error.config;

        if (error.response?.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            try {
                const newAccess = await authService.refreshToken();
                originalRequest.headers.Authorization = `Bearer ${newAccess}`;
                return apiService(originalRequest);
            } catch (refreshError) {
                console.error('Refresh token error', refreshError);
                localStorage.removeItem('access');
                localStorage.removeItem('refresh');
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);

export {apiService};

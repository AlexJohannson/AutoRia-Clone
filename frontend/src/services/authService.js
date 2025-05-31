import {apiService} from "./apiService";
import {urls} from "../constants/urls";

const authService = {
    async login(user) {
        const {data} = await apiService.post(urls.auth.login, user);
        localStorage.setItem('access', data.access);
        localStorage.setItem('refresh', data.refresh);
    },

    async refreshToken() {
        const refresh = localStorage.getItem('refresh');
        const {data} = await apiService.post(urls.auth.refresh, {refresh});
        localStorage.setItem('access', data.access);
        return data.access;
    },
    getMe() {
        return apiService.get(urls.auth.siteRole);
    },
    getSocketToken() {
        return apiService.get(urls.auth.socket);
    }
};

export {authService};

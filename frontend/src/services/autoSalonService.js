import {apiService} from "./apiService";
import {urls} from "../constants/urls";

const autoSalonService = {
    getAll(){
        return apiService(urls.auto_salon)
    }
}

export {autoSalonService}
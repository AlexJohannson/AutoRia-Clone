import {apiService} from "./apiService";
import {urls} from "../constants/urls";

const sellersService = {
    getAll(){
        return apiService(urls.sellers)
    }
}

export {sellersService}
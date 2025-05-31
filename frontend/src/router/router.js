import {createBrowserRouter, Navigate} from "react-router-dom";
import {MainLayout} from "../components/MainLayoutComponent/MainLayout";
import {SellerPage} from "../pages/SellerPage/SellerPage";
import {AutoSalonPage} from "../pages/AutoSalonPage/AutoSalonPage";
import {AdminPage} from "../pages/AdminPage/AdminPage";
import {ListingsPage} from "../pages/ListingsPage/ListingsPage";
import {LoginPage} from "../pages/LoginPage/LoginPage";


const router = createBrowserRouter([
    {
        path:'', element:<MainLayout/>,
        children:[
            {
                index:true, element:<Navigate to={'login'}/>
            },
            {
                path:'login', element:<LoginPage/>
            }
        ],
    },
    {
      path:'listing', element: <ListingsPage/>
    },
    {
        path:'sellers', element:<SellerPage/>
    },
    {
        path:'auto_salon', element:<AutoSalonPage/>
    },
    {
        path:'admin', element:<AdminPage/>
    }
])

export {router}
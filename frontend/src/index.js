import ReactDOM from 'react-dom/client';
import {RouterProvider} from "react-router-dom";
import {router} from "./router/router";
import {HeaderComponent} from "./components/HeaderComponent/HeaderComponent";
import "./App.css";
import {FooterComponent} from "./components/FooterComponent/FooterComponent";



const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
       <div className={'mini-chat-app'}>
           <HeaderComponent/>
           <RouterProvider router={router}/>
           <FooterComponent/>
       </div>

);



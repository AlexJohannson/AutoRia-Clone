import React from 'react';
import {ChatComponents} from "../../components/ChatComponets/ChatComponents";
import "./AdminPage.css";




const AdminPage = () => {
    return (
        <div className={'admin-page'}>
            <h1>Admin Page</h1>
            <div>
                <ChatComponents/>
            </div>
        </div>
    );
};

export {AdminPage};
import React from 'react';
import {ChatComponents} from "../../components/ChatComponets/ChatComponents";
import "./ListingsPage.css";




const ListingsPage = () => {
    return (
        <div className={'listings-page'}>
            <h1>Listings Page</h1>
            <div>
                <ChatComponents/>
            </div>
        </div>
    );
};

export {ListingsPage};
import React from 'react';
import {ChatComponents} from "../../components/ChatComponets/ChatComponents";
import "./SellerPage.css";


const SellerPage = () => {
    return (
        <div className={'seller-page'}>
            <h1>Seller Page</h1>
            <div>
                <ChatComponents/>
            </div>
        </div>
    );
};

export {SellerPage};
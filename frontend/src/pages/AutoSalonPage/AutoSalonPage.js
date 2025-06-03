import React from 'react';
import {ChatComponents} from "../../components/ChatComponets/ChatComponents";
import "./AutoSalonPage.css";


const AutoSalonPage = () => {
    return (
        <div className={'auto-salon-page'}>
            <h1>AutoSalon Page</h1>
            <div>
                <ChatComponents/>
            </div>
        </div>
    );
};

export {AutoSalonPage};
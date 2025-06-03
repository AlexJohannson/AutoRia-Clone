import React, {useRef, useState} from 'react';
import './ChatComponents.css';
import {useChat} from "../../hooks/useChat";

const ChatComponents = () => {
    const [room, setRoom] = useState(null);
    const roomInput = useRef();
    const [targetUser, setTargetUser] = useState(null);

    const {messages, sendMessage} = useChat(room);

    const roomHandler = () => {
        setRoom(roomInput.current.value);
    };

    const handleEnterKey = (e) => {
        if (e.key === 'Enter') {
            sendMessage(e.target.value, targetUser);
            e.target.value = '';
        }
    };

    return (
        <div className="chat-container">
            {!room ? (
                <div className="room-input">
                    <input className={'chat-room-input'} type="text" ref={roomInput} placeholder="Enter chat room..." />
                    <button className={'go-to-room'} onClick={roomHandler}>GO TO ROOM</button>
                </div>
            ) : (
                <>
                    <div className="messages">
                        {messages.map((msg, index) => (
                            <div className="message" key={index}>
                                <span
                                    className={`message-user ${targetUser === msg.userId ? 'selected' : ''}`}
                                    onClick={() => {
                                        setTargetUser(prev => prev === msg.userId ? null : msg.userId);
                                    }}
                                >
                                    {msg.username} ({msg.role})
                                </span>: {msg.message}
                            </div>
                        ))}
                    </div>
                    <div className="message-input-container">
                        <input type="text" onKeyDown={handleEnterKey} placeholder="Type your message..." />
                    </div>
                </>
            )}
        </div>
    );
};

export {ChatComponents};





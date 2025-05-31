import React, {useEffect, useRef, useState} from 'react';
import {socketService} from '../../../services/socketService';

const ChatComponents = () => {

    const [room, setRoom] = useState(null);
    const [socketClient, setSocketClient] = useState(null);
    const [messages, setMessages] = useState([]);
    const roomInput = useRef();

    useEffect(() => {
        if (room) {
            socketInit(room).then(client => setSocketClient(client));
        }
    }, [room]);

    const socketInit = async (room) => {

        const {chat} = await socketService();
        const client = await chat(room);

        client.onopen = () => {
            console.log('Chat socket connected');
        };

        client.onmessage = ({data}) => {
            const parsedData = JSON.parse(data.toString());

            const role = getUserRole(parsedData);

            setMessages(prevState => [...prevState, {
                user: parsedData.user,
                role,
                message: parsedData.message
            }]);
        };

        return client;
    };


    const getUserRole = ({is_staff, is_seller, is_auto_salon_member}) => {

        if (is_staff) return 'admin';
        if (is_seller) return 'seller';
        if (is_auto_salon_member) return 'salon_member';
        return 'user';
    };

    const roomHandler = () => {
        setRoom(roomInput.current.value);
    };

    const handleEnterKey = (e) => {
        if (e.key === 'Enter') {
            socketClient.send(JSON.stringify({
                data: e.target.value,
                action: 'send_message',
                request_id: new Date().getTime()
            }));
            e.target.value = '';
        }
    };

    return (
        <div>
            {!room ? (
                <div>
                    <input type="text" ref={roomInput} />
                    <button onClick={roomHandler}>GO TO ROOM</button>
                </div>
            ) : (
                <div>
                    {messages.map((msg, index) => (
                        <div key={index}>
                            <strong>{msg.user} ({msg.role})</strong>: {msg.message}
                        </div>
                    ))}
                    <input type="text" onKeyDown={handleEnterKey} />
                </div>
            )}
        </div>
    );
};

export {ChatComponents};



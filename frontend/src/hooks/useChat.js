import {useEffect, useState} from 'react';
import {socketService} from '../services/socketService';

const useChat = (room) => {
    const [messages, setMessages] = useState([]);
    const [socketClient, setSocketClient] = useState(null);

    useEffect(() => {
        if (!room) return;

        const connect = async () => {
            const {chat} = await socketService();
            const client = await chat(room);

            client.onopen = () => console.log('Chat socket connected');

            client.onmessage = ({ data }) => {
                const parsedData = JSON.parse(data.toString());
                const [userId, username] = parsedData.user.split('_');
                const role = parsedData.user_role || 'user';

                setMessages(prev => [...prev, {
                    user: parsedData.user,
                    userId,
                    username,
                    role,
                    message: parsedData.message
                }]);
            };

            setSocketClient(client);
        };

        connect();
    }, [room]);

    const sendMessage = (text, targetUser = null) => {
        if (!socketClient) return;

        const action = targetUser ? 'send_private_message' : 'send_message';
        const data = targetUser ? {text, userId: targetUser} : {text};

        socketClient.send(JSON.stringify({
            action,
            data,
            request_id: new Date().getTime()
        }));
    };

    return {messages, sendMessage};
};

export {useChat};

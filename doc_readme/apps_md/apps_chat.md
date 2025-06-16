Chat App:

    Main role:
        Handels chat management: chat between all registered user, ddistribution of users in the chat by roles - 
        user, seller, salon_member, admin. Creating chat rooms, the ability to write private messages to any user.
        Reverting room chat history from database fore users without the ability to view private messages if the user
        has not sent or received private messages. Ability to get all chat rooms list, delete chat room or chat 
        message. WebSocket are to sent messagest in the chat in real-time.

    Structure chat app:
        chat/
            migrations/                     -   automatic files for database update
            test/                           -   testing the functionality of the chat application
                __init__.py
                test_chat_api.py
                test_chat_models.py
                test_chat_permissions.py
                test_chat_serializers.py
            __init__.py                     -   denotes a Python package          
            apps.py                         -   Django application configuration
            consumers.py                    -   handles real-time WebSocket connections for instant communication or updates
            models.py                       -   chat model definitions
            permissions.py                  -   access settings: who can view or modify data
            routing                         -   routes WebSocket request to the desired consumer
            serializers.py                  -   data conversion for API: validation and formatting
            urls.py                         -   API endpoints routing
            views.py                        -   business logic for handling chat requests

    
    Endpoints:

        Method          Endpoints                   Descriptions
     
        GET             api/chat                    Retrieve all chat rooms list
        GET             /<int:pk>                   Retrieve chat room by ID
        DELETE          /delete/<int:pk>            Delete chat room by ID
        DELETE          /messages/delete/<int:pk>   Delete chat message by ID 
        
    
    Routing WebSocket endpoint:

        Type            Path                Description

        WebSocket       <str:room>/       Real-time create and using for chat

    Test chat app:
        docker compose run --rm app sh
        python manage.py test apps.chat.test
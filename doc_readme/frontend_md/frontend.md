Frontend (Testing Only):

    This frontend application is created exclusively for testing real-time function and integrating with the 
    backend via WebSocket and REST API. 
    
    Appointment:
        
        - obtaining an activation token

        - obtaining an recovery token

        - testing chat via WebSocket


    Technology:
        
        - React.js
        - Axios
        - React Hook Form
        - React Router DOM
        - WebSocket - via the websocket package
        - npm-watch - for dev convenience



    Structure frontend:
        frontend/
                node_modules/
                public/
                src/
                    components/
                              ChatComponents/
                                            ChatComponents.css
                                            ChatComponents.js
                              FooterComponent/
                                             FooterComponent.css
                                             FooterComponent.js
                              HeaderComponent/
                                             HeaderComponent.css
                                             HeaderComponent.js
                              LoginFormComponent/
                                             LoginFormComponent.css
                                             LoginFormComponent.js
                              MainLayoutComponent/
                                             MainLayout.js
                    constants/
                              urls.js
                    hooks/
                              useChat.js
                    pages/
                              AdminPage/
                                        AdminPage.css
                                        AdminPage.js
                              AutoSalonPage/
                                        AutoSalonPage.css
                                        AutoSalonPage.js
                              ListingPage/
                                        ListingPage.css
                                        ListingPage.js
                              LoginPage/
                                        LoginPage.css
                                        LoginPage.js
                              SellerPage/
                                        SellerPage.css
                                        SellerPage.js
                    router/
                              router.js
                    services/
                              apiService.js
                              autServise.js
                              socketService.js  
                    App.css
                    index.js
                .env
                .gitignore
                package.json
                package-lock.json



        

    Account activation testting:

        - register a new user via Postman

        - check email, will receive a letter with an activation link

        - follow the link in the browser

        - manually copy the activation token from the URL address

        - insert token into request in Postman ({{host}}/auth/activate/<str:token>)



    Password recovery testing:

        - send a password recovery request
        
        - check email, will receive a letter with an recovery link

        - follow the link in the browser

        - manually copy the recovery token from the URL adress

        - insert recovery token into request in Postman ({{host}}/auth/recovery/<str:token>)



    
    Char testing:

        Using WebSocket via Django Channels and Daphne. Socket connection implemented in a file socketService.js
        Can check the sending of the message and the reaction in real-time.

        To start testing the chat need to enter this URL http://localhost, after will be automatically redirected
        to the LoginPage http://localhost/login

        Need to register a user, seller, auto salon member and admin in Postman. Depending on which roles to test
        chat with.

        In the project all registered users are devided into roles for the convenience of testing the chat.
        A registered user automatically receives the (user) role. Seller (seller) role. Auto salon participant
        (salon_member) role. Site administrator (admin) role. 

        For each of management there is navigation in the chat where everyone gest to their own page in the chat
        according to their role. 
                                User (user) navigate to ListingsPage
                                Seller (seller) navigate to SellerPage
                                Auto salon memeber (salon_member) navigate to AutoSalonPage
                                Admin of the AutoRia Clone (admin) navigate to AdminPage


        After loggin in the chat users create chat room among themselves. This is a shared chat room where every
        user can see other users messages. Users can create other chat rooms depending on their needs.

        In a shared chat room users can also send each other private message. Private message will be labeled
        "Private". In shared chat room to send a private message to a user:
                                    Example:
                                            <your_name> (user): need to click on the <your_name> (seller) to whom
                                            be wants to send a private message. Now the <your_name> (user) can
                                            write private messages to the <your_name> (seller). If the <your_name>
                                            (seller) wants to reply to this <your_name> (user) with a private
                                            message, the <your_name> (seller) needs to click on the <your_name>
                                            (user) name and <your_name> (seller) can send private messages. To end
                                            a private conversation between <your_name> (user) and <your_name> 
                                            (seller), the <your_name> (seller) needs to click on the <your_name>
                                            (user) name again. It also works if the <your_name> (user) wants to
                                            end a private conversation with the <your_name> (seller). 

        If this was a shared chat room then private messages can only be seen by those participants who sent or
        received private messages.

    
        All chat rooms with messages are stored in the database. When a user reopens a chat room in which there 
        was messages the history of seven messages will be returned from the database. If there were private
        messages in the shared chat room, the private messages will only be returned to those participants who
        sent or received them.
    



    
    
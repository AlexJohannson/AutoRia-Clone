AutoRia Clone

AutoRia Clone - was developed for a client who owns an existing but outdated vehicle marketplace. With a rapidly 
growing user base, the client required a modern, flexible, and high-load-ready system that supports frequent 
updates, architecture-level changes, and future expansion—including integration with AWS via Docker 
containerization.
 



Technology:

    -Backend:
        -Python 3.12+;
        -Django 4+;
        -Django REST Framework;
        -JWT Authentication (Simple JWT);
        -Celery + Redis;
        -MySQL;
        -Channels + Daphne + WebSocket;
        -DRF-YASG (Swagger);

    -DevOps:
        -Docker / Docker Compose;
        -Poetry;
        -Nginx;
 
   

Core Features:

    JWT Authentification (Simple JWT):
        -Real-time Chat (WebSocket);
        -Real-time Listing Updates (WebSocket);
        -Auto Salon Invitations via WebSocket;
        -Salon Roles Management via WebSocket;
        -Roles-based user system:
            -Buyer (user);
            -Seller (user);
            -Manager (admin);
            -Administrotor(superuser);



Account Types:
    
    -Basic Account:
        -Default for all sellers with limited functionality;
    
    -Premium Account:
        -Extended features, including detailed statistics;



Auto Salon Features:

    -Auto salon creation with user role management:
        -Administrator (superuser of auto salon);
        -Manager (admin of auto salon);
        -Seller (seller of auto salon);
        -Mechanic (mechanic of auto salon);



Listings:

    -View statistics for listings;
    -Average car prices calculated by:
        -City;
        -Region;
        -Country;
    -Currency display: USD, EUR, UAH (based on PrivatBank exchange rates);
    -Automatic prohibited words check;
    -Advance listing statistics for premium account;



Scheduled Tasks (Celery):

    -Automatic currency updayes;
    -Average price calculations;
    -Automated email notifications;



Project structure:

    .venv
    backend/
        apps/
            auth/
            auto_salon/
            auto_salon_listings/
            base_account/
            car_brand/
            car_model/
            chat/
            forbiddenword/
            invitation_to_auto_salon/
            listings/
            premium_account/
            salon_role/
            sellers/
            user/
        configs/
        core/
        static/
        storage/
        templatest/
        manage.py
    client/
    doc_readme/
    frontend/
        src/
            components/
                ChatComponents/
                FooterComponents/
                HeaderComponents/
                LoginFormComponents/
                MainLayoutComponents/
            constans/
            hooks/
            pages/
                AdminPage/
                AutoSalonPage/
                ListingsPage/
                LoginPage/
                SellerPage/
            router/
            services/
            App.css
            index.js
    mysql/
    .env
    .env.example
    .gitignore
    autoria-clone.postman_collection.json
    autoRiaClone.txt
    autoRiaCloneEnglishVersion.txt
    docker-compose.yml
    Dockerfile
    nginx_conf
    poetry.lock
    pyproject.toml
    README.md
    setup.cfg



Docker services:

    -web: Django + Daphne (ASGI) server;
    -db: MySQL;
    -redis: Message broker for Celery;
    -nginx: Reverse proxy server;
    -celery: Background task processor (auto-started);
    -celery-beat: Scheduled task proccessor (auto-started);



Key Libraries:

    -Django;
    -Django REST Framework;
    -Simple JWT;
    -Celery;
    -Redis;
    -Django Celery Beat;
    -Django Celery Results;
    -Channels + Daphne + Channels Redis;
    -DRF YASG (Swagger);
    -Pillow;
    -Requests;
    -Django Filter;
    -isort;



Django Settings Highlights:

    -MySQL database (configured via enviroment variables);
    -Custom user model: UserModel;
    -Static files served via /drf-static/ (nginx);
    -Daphne server (ASGI) for WebSocket support;
    -Celery configured with Redis;



API Documentation:

    Swagger: http://localhost/api/doc
    Postman Collection: autoria-clone.postman_collection.json



Frontend Notes:
    
    -Obtain activation token via Postman and manually activate the user;
    -Obtain recovery token via Postman to reset the user password;
    -WebSocket chat testing is available;



Environment Variables (.env):

    SECRET_KEY=
    DEBUG=

    MYSQL_USER=
    MYSQL_PASSWORD=
    MYSQL_ROOT_PASSWORD=
    MYSQL_DATABASE=
    MYSQL_HOST=
    MYSQL_PORT=



Project Setup:
    
    1. Clone the repository:
        git clone https://github.com/AlexJohannson/AutoRia-Clone
        cd AutoRia-Clone
            
    2. Configure .env file based on .env.example.

    3. Build and start services:
        docker compose up --build

    4. Apply migrations:
        docker compose run --rm app sh
        python manage.py makemigrations
        python manage.py migrate

    Create superuser:
        docker compose run --rm app sh
        python manage.py createsuperuser
        email: <your_email>
        password: <your_password>



Project Test:
    
    For test all project:
        docker compose run --rm app sh
        python manage.py test



For a deeper look into the project’s functionality, please visit the doc_readme/ folder

    It includes detailed explanations of the backend, frontend, core logic, templates, storage structure and 
    configuration.



Note: For security reasons, the .env file is not included in the repository. If you'd like to run the project 
locally, feel free to reach out and request access to it.







            
Configs:

    The configs foledr contains configuration files for launching and running the project. Configs includes settings:
    Django, Celery, JWT, WebSocket (Channels), REAT Api and routing.

    Structure configs folder:
        configs/
                extra_conf/
                        __init__.py
                        celery_conf.py
                        channels_conf.py
                        email_conf.py
                        jwt_conf.py
                        rest_conf.py
                __init__.py
                asgi.py
                celery.py
                routing.py
                settings.py
                urls.py
                wsgi.py

    Celery:

        celery.py: initializetion Celery
        
        celery_conf.py: broker serrings (redis://redis:6379/0), serializers, results backend and scheduler
                        (django_celery_beat)

        beat_schedule: recurring task scheduler (avg_price_task, update_exchange_rates)


    Channels:

        asgi.py: defines protocols for ASGI (http, websocket)

        channels_conf: configuration for RedisChannelLayer, user for WebSockets

        routing.py: defines WebSocket routes for different modules (chat, listings, auto_salon_listing, salon_role, 
        invitation_to_auto_salon)

    Email:

        email_conf.py: using enviroment variables (EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_PORT, 
        EMAIL_USE_TLS) for SMTP


    JWT:

        jwt_conf.py: settings for JWT, including (ACCESS_TOKEN_LIFETIME, REFRESH_TOKEN_LIFETIME) and security
        settings (ROTATE_REFRESH_TOKENS, BLACKLIST_AFTER_ROTATION)


    REST API:
        rest_conf.py: defines REST_FRAMEWORK, authentication via JWT (DEFAULT_AUTHENTICATION_CLASSES), filtering
        (DEFAULT_FILTER_BACKENDS) and pagination


    Main files Django:

        settings.py: main settings includung database connection (DATABASES), installed applications 
        (INSTALED_APPS) and middleware (MIDDLEWARE)

        urly.py: all routes API including auth, user, sellers, listings, car_brand, car_model, forbidden_word,
        auto_salon, salon_role, invitation_to_auto_salon, auto_salon_listing, doc(Swagger), processing media
        files through static() which allows to work with files through MEDIA_URL

        asgi.py: starting ASGI - server for WebSocket

        wsgi.py: starting WSGI - server for deployment






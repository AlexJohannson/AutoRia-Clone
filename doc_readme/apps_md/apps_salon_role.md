Salon Role App:

    Main role:
        Handels salon role management: distribution of roles in the auto salon. The salon roles in the auto salon
        are four registered users on the site. This is a superuser (owner of auto salon), admin (manage of auto salo),
        seller (seller of auto salon), mechanic (mechanic of auto salon). There are no more auto salon roles and if
        a role needs to be replaced, the existing role in the auto salon mist first be deleted. WebSocket are to
        update roles in the auto salon in real-time.

    Structure salon_role app:
        salon_role/
                    migrations/             -   automatic files for database update
                    test/                   -   testing the functionality of the salon_role application
                        __init__.py
                        test_salon_role_api.py
                        test_salon_role_filter.py
                        test_salon_role_models.py
                        test_salon_role_permissions.py
                        test_salon_role_serializers.py
                    __init__.py             -   denotes a Python package
                    apps.py                 -   Django application configuration
                    consumer.py             -   handles real-time WebSocket connections for instant updates
                    filter.py               -   ordering filter by Id and role
                    models.py               -   salon_role model definitions
                    permissions.py          -   access settings: who can view or modify data
                    routing.py              -   routes WebSocket request to the desired consumer
                    serializers.py          -   data conversion for API: validation and formatting
                    urls.py                 -   API endpoints routing
                    views.py                -   business logic for handling salon_role requsts
     
    Endpoints:

        Method          Endpoints           Descriptions
        
        GET             api/salon_role      Retrieve all salon_role
        GET             /<int:pk>           Retrieve salon_role by ID
        DELETE          /<int:pk>           Delete salon_role by ID

    Routing WebSocket endpoint:
    
        Type            Path                Descriptions

        WebSocket       api/salon_role/     Real-time updates for salon roles
   
    Test salon_role app:
        docker compose run --rm app sh
        python manage.py test apps.salon_role.test
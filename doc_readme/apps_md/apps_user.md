User App:

    Main role:
        Handles user management: registration, profile viewing, status changes (blocking/unblocking, 
        assigning admin roles).
        Each user registers with an email and password after which user fills out his profile. After successful 
        registration the user will be send an email with a link to activate their profile on the site. Admin can block
        or unblock a user depending on the tasks. Superuser appoints user as site admin.

    Structure user app:
        user/
            migrations/         -   automatic files for database update
            test/               -   testing the functionality of the user application
                __init__.py        
                test_user_api.py
                test_user_filter.py
                test_user_manager.py
                test_user_model.py
                test_user_permissions.py
                test_user_serializers.py
            __init__.py         -   denotes a Python package
            apps.py             -   Django application configuration
            filter.py           -   filters for searching and sorting users
            managers.py         -   custom logic for creating users and admins
            models.py           -   user and profile model definitions
            permissions.py      -   access settings: who can view or modify data
            serializers.py      -   data conversion for API: validation and formatting
            urls.py             -   API endpoints routing
            views.py            -   business logic for handling user requsts

    Endpoints:

        Method          Entpoints           Descriptions

        GET             api/user            Retrieve all users
        POST            /registration       Register a new user
        GET             /<int:pk>           Retrieve user profile by ID
        PUT             /<int:pk>           Full update of user profile
        DELETE          /<int:pk>           Delete user
        PATCH           /block_unblock/<int:pk>     Block or unblock user
        PATCH           /make_admin/<int:pk>        Assing user as admin

    Test user app:
        docker compose run --rm app sh
        python manage.py test apps.user.test


   



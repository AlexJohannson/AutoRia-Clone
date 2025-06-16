Auth App:

    Main role:
        Handles auth management: provides authorization, activation, password recovery and issuance of token for
        access to the system and WebSocket. User login and retrieval JWT tokens. Access token update. Account 
        activation via token. Password recovery via email and token. Getting a token for WebSocket connections.
        Checking user roles on the site.

    Structure auth app:
        auth/
            migrations/                     -   automatic files for database update
            test/                           -   testing the functionality of the auth application
                __init__.py
                test_auth_api.py
                test_auth_serializers.py
            __init__.py                     -   denotes a Python package     
            apps.py                         -   Django application configuration 
            models.py                       -   not use
            serializers.py                  -   data conversion for API: validation and formatting 
            urls.py                         -   API endpoints routing
            views.py                        -   business logic for handling auth requsts

                     
    Endpoints:

        Method          Endpoinpts                          Descriptions
                        
        POST            api/auth                            User login on the site ahd get JWT token
        POST            /refresh                            Get refresh token
        PATCH           /activate/<str:token>               Activate user account with token
        POST            /recovery                           Recovery request
        POST            /recovery/<str:token>               Password recovery with token 
        GET             /socket                             Getting WebSocket token for connection            
        GET             /site_role                          Get user site role
        
   
    Test auth app:
        docker compose run --rm app sh
        python manage.py test apps.auth.test
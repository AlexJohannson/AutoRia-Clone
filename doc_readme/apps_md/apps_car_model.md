Car Model App:

    Main role:
        Handels car_model management: creating and storing car models. The condition stipulates that the seller or
        auto salon cannot create an listing with a car model that does not exist on the site. They are given a list 
        of all available car models on the site. The list of car models can be managed by both the superuser or
        admin of the site. If a seller or auto salon wants a new car model that does not exist, they can notify
        the site admin in the chat.

    Structure car_model app:
        car_model/
                migrations/                 -   automatic files for database update
                test/                       -   testing the functionality of the car_model application
                    __init__.py
                    test_model_api.py
                    test_model_filter.py
                    test_model_models.py
                    test_model_permissions.py
                    test_model_serializers.py
                __init__.py                 -   denotes a Python package
                apps.py                     -   Django application configuration
                filter.py                   -   order filtering car_model
                models.py                   -   car_model model definitions
                permissions.py              -   access settings: who can view or modify data
                serializer.py               -   data conversion for API: validation and formatting
                urls.py                     -   API endpoints routing
                views.py                    -   business logic for handling car_model requsts

    Endpoints:
        
        Method                  Endpoints               Descriptios

        GET                     api/car_model           Retrieve all models
        POST                    api/car_model           Create a mew model
        GET                     /<int:pk>               Retrieve car model by ID
        PUT                     /<int:pk>               Full update model
        PATCH                   /<int:pk>               Partial update model
        DELETE                  /<int:pk>               Delete car model
   
              
    Test car_model app:
        docker compose run --rm app sh
        python manage.py test apps.car_model.test
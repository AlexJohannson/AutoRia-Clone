Car Brand App:

    Main role:
        Handels car_brand management: creating and storing car brand. The condition stipulates that the seller or
        auto salon cannot create an listing with a car brand that does not exist on the site. They are given a list
        of all available car brand on the site. The list of car brand can be managed by both the superuser or
        admin of the site. If a seller or auto salon wants a new car brand that does not exist, they can notify
        the site admin in the chat.

    Structure car_brand app:
        car_brand/
                migrations/                 -   automatic files for database update
                test/                       -   testing the functionality of the car_brand application
                   __init__.py     
                   test_brand_api.py 
                   test_brand_filter.py 
                   test_brand_model.py 
                   test_brand_permissions.py     
                   test_brand_serializers.py
                __init__.py                 -   denotes a Python package
                apps.py                     -   Django application configuration
                filter.py                   -   order filtering car_brand
                models.py                   -   car_brand model definitions
                permissions.py              -   access settings: who can view or modify data
                serializer.py               -   data conversion for API: validation and formatting
                urls.py                     -   API endpoints routing
                views.py                    -   business logic for handling car_brand requsts
    
    Endpoints:
        
        Method                  Endpoints               Descriptios

        GET                     api/car_brand           Retrieve all car bramd
        POST                    api/car_brand           Create a mew car brand
        GET                     /<int:pk>               Retrieve car brand by ID
        PUT                     /<int:pk>               Full update car brand
        PATCH                   /<int:pk>               Partial update car brand
        DELETE                  /<int:pk>               Delete car brand
   
              
    Test car_brand app:
        docker compose run --rm app sh
        python manage.py test apps.car_brand.test
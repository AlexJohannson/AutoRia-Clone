Sellers App:

    Main role:
        Handles sellers management: create seller, seller profile viewing, buy premiun account. A registered user
        can become a seller to post listings. By default, when a user switches to a seller, they receive a basic account.
        With a basic account a seller can only publish one listing. The basic account does not provide additional views 
        listing or average prices. It is provided that the seller can buy a premium account. A seller with a premium
        account can publish listings without restrictions, receive views of listings and see average prices in 
        listing.

    Structure sellers app:
        sellers/
                migrations/             -   automatic files for database update
                test/                   -   testing the functionality of the sellers application
                    __init__.py
                    test_sellers_api.py
                    test_sellers_filter.py
                    test_sellers_models.py
                    test_sellers_permissions.py
                    test_sellers_serializers.py
                __init__.py             -   denotes a Python package
                apps.py                 -   Django application configuration
                filter.py               -   order filtering sellers by ID
                models.py               -   sellers model definitions
                permissions.py          -   access settings: who can view or modify data            
                serializers.py          -   data conversion for API: validation and formatting
                urls.py                 -   API endpoints routing
                views.py                -   business logic for handling sellers requsts

    Endpoints:

        Method          Endpoinpts          Descriptions
        
        GET             api/sellers         Retrieve all sellers
        POST            api/sellers         Register a new seller
        GET             /<int:pk>           Retrieve seller profile by ID   
        DELETE          /<int:pk>           Delete seller
        POST            /buy_premium        Buy premium account
   
    Test sellers app:
        docker compose run --rm app sh
        python manage.py test apps.sellers.test

    
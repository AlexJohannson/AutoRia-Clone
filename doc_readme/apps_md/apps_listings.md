Listings App:

    Main role:
        Handels listings management: viewing and creating listings, updating listings, adding a photo to a listing,
        checking for prohibited words, viewing and deleting inactive listings. Before publication each listings is
        checked for prohibited words. The seller can published listing three attempts. On each attempt there will 
        be a warning that prohibited words were used and how many attempts are left. After the third attempt the 
        listing will be blocked (is_active=False) and unavailable to the seller. At the same time an email will 
        be sent to the admin containing information about which seller published the listing, which listing and the 
        reason for the blocking. The admin can view the list of blocked listings and delete them. It is possible 
        to add a photo to the listing. Photos are not required, the seller decides whether to add photos to his
        listings. The seller can specify the price in the following currencies: USD (default), EUR, UAH. Other
        currencies will be converted at the PrivatBank (Ukraine) rate and shown in the listing. WebSocket are to 
        update listings in real-time.

    Structure listings app:
        listings/
                migrations/                 -   automatic files for database update
                test/                       -   testing the functionality of the listings application
                    __init__.py
                    test_listings_photo_serializers.py
                    test_listings_api.py
                    test_listings_filter.py
                    test_listings_models.py
                    test_listings_permissions.py
                    test_listings_serializers.py
                __init__.py                 -   denotes a Python package
                apps.py                     -   Django application configuration
                consumer.py                 -   handles real-time WebSocket connections for instant updates
                filter.py                   -   filters for searching and sorting listings
                models.py                   -   listings model definitions
                permissions.py              -   access settings: who can view or modify data
                routing.py                  -   routes WebSocket request to the desired consumer
                serializers.py              -   data conversion for API: validation and formatting
                urls.py                     -   API endpoints routing
                views.py                    -   business logic for handling listings requests

    Endpoints:

        Method          Endpoints                           Descriptions
     
        GET             api/listings                        Retrieve all listings
        POST            api/listings                        Publication a new listing
        GET             /<int:pk>                           Retrieve listing bi ID
        PUT             /<int:pk>                           Full update listing by ID
        DELETE          /<int:pk>                           Delete listing
        PUT             /photo/<int:pk>                     Add a photo to a listing by ID
        GET             /inactive                           Retrieve all inactive listings
        DELETE          /inactive/delete/<int:pk>           Delete inactive listing by ID

    Routing WebSocket endpoint:

        Type            Path                Description

        WebSocket       api/listings/       Real-time updates for listings

    Test listings app:
        docker compose run --rm app sh
        python manage.py test apps.listings.test
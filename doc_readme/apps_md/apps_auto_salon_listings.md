Auto Salon Listings App:

    Main role:
        Handels auto salon listings management: viewing and creating listings, updating listings, adding a photo to
        a listing, checking for prohobited words, viewing and deleting inactive listings. By default auto salons
        receive a premium account by default. When publishing an listing they immediately get access to their 
        listings views, average prices and unlimited listings posting. Before publication each listings is checked
        for prohibited words. Auto salons can published listing three attempts. On each attempt they will be a
        warning that prohibites words were used and how many attempts are left. After the third attempt the listing
        will be blocked (is_active=False) and unavailable to the auto salon. At the same time an email will be sent
        to the admin containing information about which auto salon published the listing, which listing and the
        reason for the blocking. The admin can view the list of blocket listings and delete them. It is possible
        to add a photo to the listing. Photo are not required, auto salon decides whether to add photos to his
        listings. The auto salon can specify the price in the following currencies: USD (default), EUR, UAH. Other
        currencies will be converted at the PrivatBank (Ukraine) rate and show in the listing. WebSocket are to
        update auto salon listings in real-time.

    Structure auto_salon_listings app:
        auto_salon_listings/
                            migrations/                 -   automatic files for database update
                            test/                       -   testing the functionality of the auto_salon_listings application
                                __init__.py
                                test_salon_listings_models.py
                                test_salon_listings_api.py
                                test_salon_listings_filter.py
                                test_salon_listings_permissions.py
                                test_salon_listings_photo_serializers.py
                                test_salon_listings_serializers.py
                            __init__.py                 -   denotes a Python package
                            apps.py                     -   Django application configuration
                            consumer.py                 -   handles real-time WebSocket connections for instant updates
                            filter.py                   -   filters for searching and sorting auto_salon_listings
                            models.py                   -   auto_salon_listings model definitions
                            permissions.py              -   access settings: who can view or modify data
                            routing.py                  -   routes WebSocket request to the desired consumer
                            serializers.py              -   data conversion for API: validation and formatting
                            urls.py                     -   API endpoints routing
                            views.py                    -   business logic for handling auto_salon_listings requests

    Endpoints:

        Method          Endpoints                                     Descriptions
     
        GET             api/auto_salon_listing                        Retrieve all auto salon listings
        POST            api/auto_salon_listing                        Publication a new auto salon listing
        GET             /<int:pk>                                     Retrieve auto salon listing bi ID
        PUT             /<int:pk>                                     Full update auto salon listing by ID
        DELETE          /<int:pk>                                     Delete auto salon listing
        PUT             /photo/<int:pk>                               Add a photo to a auto salon listing by ID
        GET             /inactive                                     Retrieve all inactive auto salon listings
        DELETE          /inactive/delete/<int:pk>                     Delete inactive auto salon listing by ID

    Routing WebSocket endpoint:

        Type            Path                            Description

        WebSocket       api/auto_salon_listing/         Real-time updates for auto salon listings

    Test auto_salon_listings app:
        docker compose run --rm app sh
        python manage.py test apps.auto_salon_listings.test
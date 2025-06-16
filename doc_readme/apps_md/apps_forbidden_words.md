Forbidden Words App:

    Main role:
        Handels forbidden words management: record and save forbidden words, delete and update forbidden words.
        Superuser or admin of site can dicede and correct which words they consider bad, update or delete or fill
        in a table to store them in the database for further validation of listings.

    Structure forbiddenword app:
        forbiddenword/
                    migrations/                 -   automatic files for database update
                    test/                       -   testing the functionality of the forbiddenword application
                        __init__.py
                        test_words_api.py
                        test_words_model.py
                        test_words_permissions.py
                        test_words_serializers.py
                    __init__.py                 -   denotes a Python package
                    apps.py                     -   Django application configuration
                    models.py                   -   forbiddenword model definitions
                    permissions.py              -   access settings: who can view or modify data
                    serializers.py              -   data conversion for API: validation and formatting
                    urls.py                     -   API endpoints routing
                    views.py                    -   business logic for handling forbiddenword requests

    Endpoints:

        Method          Endpoints                   Descriptions
     
        GET             api/forbidden_word          Retrieve all forbidden words
        POST            api/forbidden_word          Record forbidden words to tadle for storage
        GET             /<int:pk>                   Retrieve forbidden word by ID
        PUT             /<int:pk>                   Update forbidden word by ID
        PATCH           /<int:pk>                   Partial update forbidden word by ID
        DELETE          /<int:pk>                   Delete forbidden word

    Test forbiddenword app:
        docker compose run --rm app sh
        python manage.py test apps.forbiddenword.test

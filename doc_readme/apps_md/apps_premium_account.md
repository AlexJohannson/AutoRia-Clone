Premium Account App:

    Main role:
        Responsible for storing and recording information about premium account of sellers and auto salon.

    Structure premium_account app:
        premium_account/
                        migrations/         -   automatic files for database update
                        test/               -   testing the functionality of the premium_account application
                            __init__.py
                            test_premium_account_models.py
                        __init__.py         -   denotes a Python package
                        apps.py             -   Django application configuration
                        models.py           -   premium_account model definitions
                        views.py            -   not use

     Test premium_account app:
        docker compose run --rm app sh
        python manage.py test apps.premium_account.test
Base Account App:

    Main role:
        Responsible for storing and recording information about bace accout of sellers.

    Structure base_account app:
        base_account/
                    migration/                          -   automatic files for database update
                    test/                               -   testing the functionality of the base_account application
                        __init__.py
                        test_base_account_models.py
                    __init__.py                         -   denotes a Python package
                    apps.py                             -   Django application configuration
                    models.py                           -   base_account model definitions                
                    views.py                            -   not use

    Test base_account app:
        docker compose run --rm app sh
        python manage.py test apps.base_account.test
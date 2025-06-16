Auto Salon App:

    Main role:
        Handels auto salon management: create auto salon, retrieve auto salon list or auto salon profile by ID,
        delete auto salon, update auto salon. A registered user car create a auto salon. It is envisaged that since 
        a auto salon needs more functionality, creating a auto salon on the AutoRia Clone site is buying a auto
        salon by default. By default auto salon immediately receives a premium account. When creating auto salon
        the owner of the auto salon receives the superuser role by default. A auto salon can accept four roles:
        superuser by default, admin, seller and mechanic by invitation.

    Structure auto_salon app:
        auto_salon/
                  migrations/               -    automatic files for database update
                  test/                     -    testing the functionality of the auto_salon application 
                       __init__.py 
                       test_auto_salon_api.py 
                       test_auto_salon_filter.py 
                       test_auto_salon_models.py 
                       test_auto_salon_permissions.py 
                       test_auto_salon_serializers.py 
                  __init__.py               -     denotes a Python package    
                  apps.py                   -     Django application configuration    
                  filter.py                 -     order filtering auto_salon     
                  models.py                 -     auto_salon model definitions
                  permissions.py            -     access settings: who can view or modify data     
                  serializers.py            -     data conversion for API: validation and formatting    
                  urls.py                   -     API endpoints routing    
                  views.py                  -     business logic for handling auto_salon requsts    


    Endpoints:

        Method          Endpoinpts              Descriptions
        
        GET             api/auto_salon          Retrieve all auto salon list
        POST            api/auto_salon          Create a new auto salon
        GET             /<int:pk>               Retrieve auto salon by ID
        PUT             /<int:pk>               Update auto salon
        DELETE          /<int:pk>               Delete auto salon
        
   
    Test auto_salon app:
        docker compose run --rm app sh
        python manage.py test apps.auto_salon.test
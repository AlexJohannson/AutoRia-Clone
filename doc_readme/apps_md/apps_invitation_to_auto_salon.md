Invitation To Auto Salon App:

    Main role:
        Handels invitation_to_auto_salon management: view invitations, create a invitationa, approve invitations,
        delete invitations. Invitations to the auto salon can only be made by registered users in three roles:
        admin, seller, mechanic. When creating a auto salon the registered user becomes a superuser by default. 
        A superuser or admin of auto salon can approve or reject an invitation to specific role. It is foreseen 
        that it is not possible to create an invitation to a auto salon for a role that is already taked in this 
        auto salon. WebSocket are to update invitation to auto salon in real-time

    Structure invitation_to_auto_salon app:
        invitation_to_auto_salo/
                                migrations/         -   automatic files for database update
                                test/               -   testing the functionality of the invitation_to_auto_salon application
                                    __init__.py
                                    test_invitation_api.py
                                    test_invitation_models.py
                                    test_invitation_permissions.py
                                    test_invitation_serializers.py
                                __init__.py         -   denotes a Python package
                                apps.py             -   Django application configuration
                                consumer.py         -   handles real-time WebSocket connections for instant updates
                                models.py           -   invitation_to_auto_salon model definitions
                                permissions.py      -   access settings: who can view or modify data
                                routing.py          -   routes WebSocket request to the desired consumer
                                serializers.py      -   data conversion for API: validation and formatting
                                urls.py             -   API endpoints routing
                                views.py            -   business logic for handling invitation_to_auto_salon requests

    Endpoints:

        Method          Endpoints                               Descriptions
        GET             api/invitation_to_auto_salon            Retrieve all invitations list
        POST            api/invitation_to_auto_salon            Create a new invitation to auto salon
        PATCH           /<int:pk>/approved                      Approve invitation to auto salon
        DELETE          /delete/invitation/<int:pk>             Delete invitation to auto salon by ID
    

    Routing WebSocket endpoint:

        Type            Path                                Description

        WebSocket       api/invitation_to_auto_salon/       Real-time updates for invitation_to_auto_salon

    Test invitation_to_auto_salon app:
        docker compose run --rm app sh
        python manage.py test apps.invitation_to_auto_salon.test
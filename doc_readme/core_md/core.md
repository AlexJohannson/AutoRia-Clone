Core:

    The core folder is responsible for business logic, error handling, middleware, services and background tasks
    in the project. Core contains key logic that ensures the correct operation of the entire project.

    Main function:

        Services: logics for email, JWT, files, exchange rates

        Error handling: custom exceptions, error handling

        Middleware: for check WebSocket request

        Background tasks: Celery

        Pagination: pagination for DRF

        Management - teams: for check database availability


    Structure core folder:

        core/
            enums/
                __init__.py
                action_token_enum.py
                regex_enum.py
            exceptions/
                        __init__.py
                        jwt_exception.py
            exchange_state/
                            __init__.py
                            exchange_state.py
            handlers/
                    __init__.py
                    error_handler.py
            management/
                       commands/
                                __init__.py
                                wait_db.py
                       __init__.py
            middleware/
                      __init__.py
                      socket_middleware.py  
            migrations/
                        __init__.py
            services/
                    __init__.py
                    email_service.py
                    exchange_service.py
                    file_service.py
                    jwt.service.py
                    listing_service.py
                    listing_validation_service.py
            tasks/
                __init__.py
                avg_price_task.py
                exchange.py
                send_auto_salon_create_email_task.py
                send_auto_salon_listing_publication_email_task.py
                send_blocked_auto_salon_listing_email_task.py
                send_blocked_listing_due_bad_words_email_task.py
                send_create_admin_task.py
                send_delete_auto_salon_task.py
                send_delete_invitation_email_task.py
                send_deleted_auto_salon_listing_email_task.py
                send_join_request_approved_email_task.py
                send_join_request_email_task.py
                send_listing_deleted_email_task.py
                send_listing_publication_email_task.py
                send_premium_activate_email_task.py
                send_role_deleted_email_task.py
                send_seller_create_email_task.py
                send_seller_deleted_email_task.py
                send_user_blocked_email_task.py
                send_user_delete_email_task.py
                send_user_unblocked_email_task.py
                send_welcome_email_task.py
            __init__.py
            apps.py
            models.py
            paginations.py


        Enums:
        
            action_token_enum.py: file contains ActionTokenEnum that define the types of tokes and timedelta
                ACTIVATE: the account activation token is valid for 30 minutes
                RECOVERY: password recovery token valid for 30 minutes
                SOCKET: the token for WebSocket request is valid for 10 seconds
            In each case the token type and lifetime (timedelta) are stored



        RegexEnum:
            regex_enum.py: the file contains RegexEnum that contains regular expression patterns for data validation:
                NAME, SURNAME, STREET, CITY, REGION, COUNTRY, GENDER: text field validation
                CITY_LISTING, REGION_LISTING, COUNTRY_LISTING: geographic data validation
            Each element comtains regular expressions for valodation and error reporting



        Exceptions:
            jwt_exception: costom exception used for JWT



        Exchange state:
            exchange_state.py: dictionary that stores current exchange rates (USD_UAH, EUR_UAH, USD_EUR, EUR_USD, 
                                updated)
            Used for currency conversion in the project



        Handlers:
            error_handler.py: global error handling API, used exception_handler from DRF, has a special handler 
                                jwt_exception_handler that returns status 401 in case of problems with JWT



        Management:
            management/
                    commands/
                            wait_db.py: command that checks database availability before running. Executes 
                            connection.ensure_connection(). If database is unavailable waits 3 second and tries 
                            again. After successful connection print 'Database available!'



        Middlewares:
            socket_middleware.py: for user validation in WebSocket requests. Uses get_user() that verifies the 
                                    token through JWTService.verify_token. Add scope['user'], that allows to
                                    recognize authorized users



        Services:

            email_service.py: class for sending emails, send_email() - uses Celery for asynchronous sending. 
                                register() - send email for activate account, recovery() - send email for recovery
                                password


            exchange_servose.py: loads currency rates from the PrivatBank (Ukraine) API, calculates the ratio.
                                    Used to convert currencies in the project.


            file_service.py: forms a shortcut to save photos in a folder:
                                    storage/
                                            listings/


            jwt_service.py: ActionToken - base token with blaclist support (BlacklistMixin),
                            RecoveryToken / ActivateToken / SocketToken - token classes with corresponding expiration
                            dates,
                            JWTService - token management:
                                        create_token () - creating a token for the user
                                        verify_token () - token verification and user retrieval


            listing_service.py: calculate_prices () - price conversion from USD/EUR/UAH
                                check_seller_listing_limit () - check listings publication limit for sellers
                                update_listing_views () - update views for listings (daily, weekly, monthly)


            listing_validation_service.py: contains_forbidden_word () - checks the text for prohibited words from 
                                            Forbiddenwords database



        

        apps.py: Django application configuration 



        models.py: 
                BaseModel: abstract model for all models in the project,
                            contains two fields:
                                                created_at: creation date
                                                updated_at: date of last record update



        
        paginations.py: class for pagination of lists in DRF
                        Determines:
                                    page size = 6, maximum page size = 10;
                                    parameter size: allows users to resize the page
                                    automatic sorting: if queryser has no sort, adds order_by('id')
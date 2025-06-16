Tasks:

    Description of asynnchronous Celery tasks in the project

    Structure tasks folder:

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


        avg_price_task.py: a Celery background task that calculates the average price of listings in a specific city,
                            region, country. Browses active listings from sellers with a premium account. Uses a
                            aggregate(Avg('price')) to determine the average value. Update the average prices fields
                            avg_city_price, avg_region_price, avg_country_price in the model.



        exchange.py: requests the PrivatBank (Ukraine) API to obtain currency rates (USD, EUR). Form a dictionary rates
                        that containing currency ratios UAH, USD, EUR. Updates the global status of exchange rates
                        exchange_state.exchange_rates. Calculates cross rates USD-EUR, EUR-USD.



        send_auto_salon_create_email_task.py: sends an email for after creating a auto salon. Uses EmailService to
                                                to send emails to new users. 
                                                Template contains:
                                                                    - name of user (name)
                                                                    - name of auto salon (auto_salon_name)
                                                                    - location of auto salon (location)
                                                Used to confirm the creation of a auto salon.



        send_auto_salon_listing_publication_email_task.py: send an email for after publication the auto salon listings.
                                                            Uses EmailService to send emails to auto salon.
                                                            Template contains:
                                                                            - name of user (name)
                                                                            - brand of car (car_brand)
                                                                            - model of car (car_model)
                                                                            - price of car (price)
                                                            Used to notify the owner of listing that their listing has
                                                            been successfully published



        send_blocked_auto_salon_listing_email_task.py: sending an email after blocking listing that failed the check
                                                        for prohibited words. Used a EmailService to send emails for
                                                        owners of listings.
                                                        Template contains:
                                                                    - ID of listings (listing_id)
                                                                    - name of auto salon (auto_salon_name)
                                                                    - reason for blocking (description)
                                                        Used to notify admin that a auto salons listing has been blocked.



        send_blocked_listing_due_bad_words_email_task.py: sending am email after blocking listing that failed the check
                                                            for prohibited words. Used a EmailServise to send emails
                                                            for owners of listing.
                                                            Template contains:
                                                                        - ID of listing (listing_id)
                                                                        - name of seller (seller_name)
                                                                        - reason of blocking (description)
                                                            Used to notify admin that a sellers listing has been blocked.
        


        send_create_admin_task.py: sending an email to a user when a superuser has appointed them as a admin. Used a 
                                    EmailService to send emails for users.
                                    Template contains:
                                                    - name of user (name)
                                    Used to notify new admins of their appointment.



        send_delete_auto_salon_task.py: sending an email after deleting a auto salon. Used a EmailService to send 
                                        email to owner (superuser of auto salon) or admin of auto salon.
                                        Template contains:
                                                        - name of user (name)
                                                        - name of auto salon (auto_salon_name)
                                                        - location of auto salon (location)
                                        Used to notify users after successful removal of auto salon.



        send_delete_invitation_email_task.py: sending an email after to the user that their invitation has been revoked.
                                                Used EmailService to send an email to user.
                                                Template contains:
                                                                - name of user (name), whose invitation was revoked
                                                                - name of auto salon (auto_salon_name)
                                                Used to notify user after a auto salon invitation has been revoked.



        send_deleted_auto_salon_listing_email_task.py: sending an email after deleted the listing in the auto salon.
                                                        Used EmailService to send an email to member of auto salon.
                                                        Template contains:
                                                                        - name of user (name)
                                                                        - brand of car (brand)
                                                                        - model of car (car_model)
                                                                        - price of car (price)
                                                        Used to notify memeber of auto salon to confirm successful
                                                        listing removal.



        send_join_request_approved_email_task.py: sending am email to the user whose application was approved. Used
                                                    EmailServise to send an email to user.
                                                    Template contains:
                                                                    - name of user (name)
                                                                    - name of auto salon (auto_salon_name)
                                                                    - location of auto salon (location)
                                                                    - confirmation time of invitation (updated_at)
                                                    Used to notify the user about successful confirmation of the 
                                                    application to the auto salon.



        send_join_request_email_task.py: sending an email about a new request to join the auto salon. Used EmailServise
                                        to send an email to user.
                                        Template contains:
                                                        - name of user (name)
                                                        - role in the auto salon (role)
                                                        - name of auto salon (auto_salon_name)
                                                        - location of auto salon (location)
                                                        - request made (created_at)
                                        Used to notify the user about a successfully made request to join the auto salon.



        send_listing_deleted_email_task.py: sending an email after deleted the listing for seller. Used EmailService to
                                            send an email to the seller.
                                            Template contains:
                                                            - name of seller (name)
                                                            - brand of car (brand)
                                                            - model of car (car_model)
                                                            - price of car (price)
                                            Used to notify the seller to confirm successful removal of the listing.



        send_listing_publication_email_task.py: sending an email for after publication the sellers listings. Used
                                                EmailService to send an email to the seller.
                                                Template contains:
                                                                - name of seller (name)
                                                                - brand of car (car_brand)
                                                                - model of car (car_model)
                                                                - price of car (price)
                                                Used to notify the seller to confirm successful listing posting.



        send_premium_activate_email_task.py: sending an email to the seller after purchasing a premium account. Used
                                            EmailServise to send an email to the seller.
                                            Template contains:
                                                            - name of seller (name)
                                            Used to notify the seller about the seccessful activation of the 
                                            premium account.



        send_role_deleted_email_task.py: sending an email to a user after removing their role from the auto salon.
                                        Used EmailService to send an email to the user.
                                        Template contains:
                                                        - name of user (name)
                                                        - name of auto salon (auto_salon_name)
                                                        - role in auto salon (role)
                                        Used to notify the user of confirmation of successful removal of their role 
                                        from the auto salon.



        send_seller_create_email_task.py: sending an email to a user who has just registered as a seller. Used
                                            EmailService to send an emai to the user.
                                            Template contains:
                                                            - name of user (name)
                                            Used to notify the user after successfully registering their account 
                                            as a seller.



        send_seller_deleted_email_task.py: sending an email to user removal his account as a seller. Used EmailService
                                            to send an email to the user.
                                            Template contains:
                                                            - name of user (name)
                                            Used to notify the user about the seccessful deletion of their 
                                            seller account.



        send_user_blocked_email_task.py: sending an email to user about blocked his account. Used EmailService to send
                                            an email to the user. 
                                            Template contains:
                                                            - name of user (name)
                                            Used to notify the user that their account has been blocked.



        send_user_delete_email_task.py: sending am email to the user after deleting his account. Used EmailService to
                                        send an email to the user. 
                                        Template contains:
                                                        - name of user (name)
                                        Used to notify the user of confirmation of successful deletion of their account.



        send_user_unblocked_email_task.py: sending an email to the user about unblocked his account. Used EmailService
                                            to send an email to the user.
                                            Template contains:
                                                            - name of user (name)
                                            Used to notify the user that their account has been unblocked.



        send_welcome_email_task.py: sending an email to the user after registration on the AutoRia Clone site. Used
                                    EmailService to send an email to the user.
                                    Template contains:
                                                    - name of user (name)
                                    Used to notify the user of successful registration on the AutoRia Clone site.



        



        




        
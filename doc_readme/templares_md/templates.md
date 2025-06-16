Templates:

    The directory contains HTML templates for automatic email messages sent to users in various scenarios of working
    with the platform. Django templates are used for dynamic content generation. Rendered via EmailService.send_email ().
    They are intended for use in background Celery tasks.


    Structure templates folder:
        templates/
                auto_salon_listing_deleted.html             -   notification about the removal of a auto salons listing
                auto_salon_listing_publication.html         -   notification of successful publication of auto salons
                                                                listings
                base.html                                   -   base HTML template
                blocked_auto_salon_listing.html             -   notification to admin about blocking an auto salons 
                                                                listing
                blocket_listing.html                        -   notification to admin about blocking sellers listing
                create_admin.html                           -   congratulations to the new admin
                create_auto_salon.html                      -   notification about the creation of a new auto salon
                create_premiun_account.html                 -   notification for the seller about purchasing a
                                                                premium account
                delete_auto_salon.html                      -   confirmation of auto salon deletion
                delete_email.html                           -   notification about users account deletion from the site
                delete_invitation.html                      -   canceling an invitation to a auto salon
                delete_role.html                            -   email about removing a role from the auto salon
                join_request_approved_email.html            -   confirmation of approval of the role in the auto salon
                join_request_email.html                     -   notification of a new request to join the auto salon
                listing_deleted.html                        -   notification to the seller about successful removal
                                                                of the listing
                listing_publication.html                    -   notification to the seller about successful publication
                                                                listing
                recovery.html                               -   password recovery email
                register.html                               -   account activation email
                seller_create.html                          -   notification to the user about the successful regiatration
                                                                of his account as a seller
                seller_deleted.html                         -   confirmation of successful deletion of the sellers
                                                                account
                user_blocked.html                           -   email to the user about blocking his account
                user_unblocked.html                         -   email to the user about unblocking his account
                welcome.html                                -   greetings to the user
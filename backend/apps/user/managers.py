from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email=None, password=None, **extra_fields):

        if not email:
            raise ValueError('User must have an email address')

        if not password:
            raise ValueError('User must have a password')


        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', False)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user


    def create_superuser(self, email=None, password=None, **extra_fields):

        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('status', 'active')

        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser must be is_active')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be is_staff')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must be is_superuser')

        user = self.create_user(email=email, password=password, **extra_fields)

        return user

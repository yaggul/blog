from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):

    def __create_user(self, email, password,
                      is_staff=False, is_active=False, is_superuser=False, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff,
                          is_active=is_active,
                          is_superuser=is_superuser,
                          **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **kwargs):
        return self.__create_user(email, password, is_staff=False, is_active=True,
                                  is_superuser=False, **kwargs)

    def create_superuser(self, email, password, full_name=''):
        return self.__create_user(email, password, is_staff=True,
                                  is_active=True, is_superuser=True)

    def create(self, **kwargs):
        return self.create_user(**kwargs)

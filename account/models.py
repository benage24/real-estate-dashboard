from __future__ import unicode_literals

from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
import django.utils.translation
class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self,username, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """

        # if not email:
        #     raise ValueError('The given email must be set')
        if not username:
            raise  ValueError('Users must have username')
        # email = self.normalize_email(email)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    #
    # def create_user(self,username, email, password=None, **extra_fields):
    #     extra_fields.setdefault('is_superuser', False)
    #     return self._create_user(email, password, **extra_fields)

    def create_superuser(self,username, password, **extra_fields):
        # email = self.normalize_email(email)
        user=self.create_user(password=password,username=username)
        user.is_superuser=True
        user.is_active=True
        user.is_staff=True
        user.is_admin=True
        user.save(using=self._db)
        #create superuser with all
        return user



class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(('email address'), unique=True)
    username = models.CharField(('username'),unique=True, max_length=30, blank=True)

    first_name = models.CharField(('first name'), max_length=30, blank=True)
    last_name = models.CharField(('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(('date joined'), auto_now_add=True)
    is_active = models.BooleanField(('active'), default=True)
    is_staff = models.BooleanField(('staff'), default=True)
    is_admin = models.BooleanField(('admin'), default=True)
    is_superuser = models.BooleanField(('superuser'), default=True)



    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    # USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')

    def __str__(self):
       return f" {self.get_full_name()}"

    def has_perms(self, perm_list, obj=None):
        return self.is_admin
    def get_status(self):
        status_obj={
            "is_admin",
            "is_superuser",
            "is_active"
        }
        if self.is_active and self.is_admin and self.is_superuser:
            return  status_obj
        elif self.is_active:
            return f"is_active"
        elif self.is_superuser:
            return f"self.is_superuser"
        elif elf.is_admin :
            return f"is_admin"

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def is_staff(self):
        return self.is_staff
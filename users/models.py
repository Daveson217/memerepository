# Python
from pathlib import Path

# Django
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin,
)
from django.utils import timezone
from django.utils.translation import gettext, gettext_lazy as _

# App

class UserManager(BaseUserManager):
    """
    Custom User Model manager.
    It inherits from BaseUserManager, and has 3 functions, 
    create_user(), create_staffuser(), and create_superuser()
    It requires email field.
    """
    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        now = timezone.now()
        email = self.normalize_email(email)
        user = self.model(
            email=email,            
            is_staff=is_staff, 
            is_active=True,
            is_superuser=is_superuser, 
            last_login=now,
            date_joined=now, 
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        return self._create_user(email, password, False, False, **extra_fields)

    def create_staffuser(self, email, password, **extra_fields):
        """
        Creates and saves a staff user with the given email and password.
        """
        user=self._create_user(email, password, True, False, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        user=self._create_user(email, password, True, True, **extra_fields)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=70, blank=False, default="")        
    last_name = models.CharField(max_length=70, blank=False, default="")  
    #display_name = models.CharField(max_length=70, blank=True, unique=False, default="")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) # a admin user; non super-user
    is_superuser = models.BooleanField(default=False) # a superuser
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)           
    
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name'] # Email & Password are required by default.
    
    objects = UserManager()
    
    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')
        abstract = False
    
    def __str__(self):              
        return self.email
    
    def get_absolute_url(self):
        return "/accounts/%i/" % (self.pk)        
    
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])
    
    def natural_key(self):
        return (self.email,)
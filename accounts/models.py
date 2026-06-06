from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        '''Creates and saves a User with the given email and password'''
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        '''Creates and saves a superuser with the given email and password'''
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class Department(models.Model):
    '''Model representing a department within the organization'''
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)   

    def __str__(self):
        return self.name
    
class User(AbstractBaseUser):
    '''Custom user model extending Django's AbstractBaseUser'''

    ROLE_CHOICES = (
        ('employee', 'Employee'),
        ('hr', 'HR'),
        ('admin', 'Admin'),
    )

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)

    has_perm = lambda self, perm, obj=None: self.is_superuser
    has_module_perms = lambda self, app_label: self.is_superuser

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
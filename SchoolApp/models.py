from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import PermissionsMixin, BaseUserManager
from django.contrib.auth.base_user import AbstractBaseUser


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):  # These fields tie to the roles!
    class Meta:  

         
        verbose_name = 'user'
        verbose_name_plural = 'users'

    ROLE_CHOICES = (
        
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent'),
    )

    role = models.CharField(max_length=15, choices=ROLE_CHOICES)


    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    is_staff = models.BooleanField(default=False)
    is_superuser  = models.BooleanField(default=False)  

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects= UserManager()

    def __str__(self):
        return self.first_name+self.last_name


class Cls(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Student(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    clss = models.ForeignKey(Cls, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name

class Parent(models.Model):
   
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name

class Teacher(models.Model):
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    clss = models.ManyToManyField(Cls)

    def __str__(self):
        return self.user.first_name


        



from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import datetime, timedelta
from re import compile as re_compile


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        '''Create and saves a new user'''
        if not email:
            raise ValueError('User must have an email address')
        if not password:
            raise ValueError('User needs a password')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def validate_user_info(self, postData, user=None, errors={}):
        EMAIL_REGEX = re_compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+.[a-zA-Z]+$'
        )
        # First and last name validations
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First name must be 2 or more characters'
        elif len(postData['first_name']) > 45:
            errors['first_name'] = 'First name must be 45 or less characters'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name must be 2 or more characters'
        elif len(postData['first_name']) > 45:
            errors['last_name'] = 'Last name must be 45 or less characters'

        # Email validation
        # Check if email exists in DB
        email_check = self.filter(email=postData['email'])
        if len(email_check) > 0:
            if not user or user.email != email_check[0].email:
                errors['email'] = "Email already in use"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email address!"

        return errors

    def validate_password(self, postData, errors={}):
        # Password validations
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be 8 opr more characters'
        elif(postData['password'] != postData['confirm_password']):
            errors['password'] = 'Passwords must match'

        return errors

    def validate_register(self, postData):
        errors = {}
        self.validate_user_info(postData, errors)
        self.validate_password(postData, errors)

        # Birthdate validation
        todaysDate = datetime.now().date()
        dob = datetime.strptime(postData['dob'], '%Y-%m-%d').date()
        if todaysDate < dob:
            errors['birthday'] = 'Birthday must be in the past'
        elif todaysDate - dob < timedelta(days=365*18):
            errors['birthday'] = 'Must be 18 years old to create an account'

        return errors


class User(AbstractBaseUser):
    '''Custom user model supporting using email instead of username'''
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

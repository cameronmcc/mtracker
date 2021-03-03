from django.db import models
import re

class UserManager(models.Manager):
    def validate_register(self, post_data):
        errors = {}
        if len(post_data['first_name']) > 50:
            errors['first_name'] = "First name must be shorter than 50 characters."
        if len(post_data['first_name']) < 3:
            errors['first_name'] = "First name must be longer than 3 characters."
        if len(post_data['last_name']) > 50:
            errors['last_name'] = "Last name must be shorter than 50 characters."
        if len(post_data['last_name']) < 3:
            errors['last_name'] = "Last name must be longer than 3 characters."
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):    
            errors['email'] = "Invalid email address!"
        user_list = User.objects.filter(email = post_data['email'])
        if len(user_list) > 0:
            errors['email'] = "Email already taken."
        if len(post_data['password']) < 8:
            errors['password'] = "Create a stronger password longer than 8 characters."
        if post_data['password'] != post_data['confirm_password']:
            errors['password'] = "passwords do not match"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
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

class MessageManager(models.Manager):
    def validate_message(self, post_data):
        errors = {}
        if len(post_data['message']) > 300:
            errors['message'] = "Message must be shorter than 300 characters."
        if len(post_data['message']) < 3:
            errors['message'] = "Message must be longer than 3 characters."


class TicketManager(models.Manager):
    def validate_ticket(self, post_data):
        errors = {}
        if len(post_data['task']) > 50:
            errors['task'] = "Task must be shorter than 50 characters."
        if len(post_data['task']) < 3:
            errors['task'] = "Task must be longer than 3 characters."
        if len(post_data['description']) > 500:
            errors['description'] = "Description must be shorter than 500 characters."
        if len(post_data['description']) < 3:
            errors['description'] = "Description must be longer than 3 characters."
        
class ChatRoomValidator(models.Manager):
    def validate_chat(self, post_data):
        errors = {}

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    user_level = models.IntegerField()
    
    # messages_created = list of messages this user started
    # past_messages = list of all past messages associated with this user
    # created_chatrooms = list of chatrooms created by this user
    # joined_chatrooms = list of chatrooms joined by this user
    # created_tickets = list of tickets created by user
    # current_tickets = list of tickets assigned to user

    objects = UserManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
    message = models.CharField(max_length=500)

    message_creator = models.ForeignKey('User', related_name="messages_created", on_delete = models.CASCADE)
    chatroom = models.ForeignKey('ChatRoom', related_name="past_messages", on_delete = models.CASCADE, null=True)
    ticket_chat = models.ForeignKey('Ticket', related_name="past_messages", on_delete = models.CASCADE, null=True)
    
    objects = MessageManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ChatRoom(models.Model):
    User1 = models.ForeignKey('User', related_name="created_chatrooms", on_delete = models.CASCADE)
    User2 = models.ForeignKey('User', related_name="joined_chatrooms", on_delete = models.CASCADE)

    objects = ChatRoomValidator()

    #past_messages = list of users' message history

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Ticket(models.Model):
    task = models.CharField(max_length=50)
    description = models.CharField(max_length=600)
    completed = models.BooleanField()
    
    Admin_creator = models.ForeignKey('User', related_name="created_tickets", on_delete = models.CASCADE)
    assigned_user = models.ForeignKey('User', related_name="current_tickets", on_delete = models.CASCADE)

    # past_messages = list of messages associated with this ticket

    objects = TicketManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import BaseUserManager, Permission
from django.db import models


# Roles Model
class Roles(models.Model):
    role_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    date_inserted = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name


# Users Model

class UsersManager(BaseUserManager):

    def get_by_natural_key(self, email):
        """
        Returns the user with the given natural key (email).
        """
        return self.get(email=email)


class Users(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)  # Keep if needed, otherwise remove
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)  # Set on_delete behavior
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=128)  # Change field type and max_length
    contact_details = models.CharField(max_length=255, blank=True, null=True)
    date_inserted = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')  # Change related_name
    objects = UsersManager()

    USERNAME_FIELD = 'email'  # Update username field

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.name

    class Meta:
        managed = True


# Clubs Model
class Clubs(models.Model):
    club = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True)  # Use user_id as PK
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    accepting_members = models.BooleanField()
    image = models.BinaryField(blank=True, null=True)
    date_inserted = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)
    members = models.ManyToManyField(Users, related_name='members')

    def __str__(self):
        return self.name


# ClubMembers Model
class ClubMembers(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    club = models.ForeignKey(Clubs, on_delete=models.CASCADE)
    date_inserted = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"User: {self.user}, Club: {self.club}"


# AccountRequests Model
class AccountRequests(models.Model):
    a_request_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255, unique=True)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)  # Set on_delete behavior
    date_inserted = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.email


# ClubRequests Model
class ClubRequests(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    club = models.ForeignKey(Clubs, on_delete=models.CASCADE)
    date_inserted = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"User: {self.user}, Club: {self.club}"


# Events Model
class Events(models.Model):
    event_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    club = models.ForeignKey(Clubs, on_delete=models.CASCADE)  # Set on_delete behavior
    event_time = models.DateTimeField()  # Use DateTimeField for time
    venue = models.CharField(max_length=255)
    date_inserted = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"Title: {self.title}"


# EventRequests Model
class EventRequests(models.Model):
    event = models.ForeignKey('Events', models.DO_NOTHING)
    user = models.ForeignKey(Users, models.DO_NOTHING)
    date_inserted = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import BaseUserManager, Permission
from django.db import models


class Roles(models.Model):
    role_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    date_inserted = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name


class UsersManager(BaseUserManager):

    def get_by_natural_key(self, email):
        """
        Returns the user with the given natural key (email).
        """
        return self.get(email=email)


class Users(AbstractBaseUser):
    user_id = models.AutoField(primary_key=True)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=128)
    contact_details = models.CharField(max_length=255, blank=True, null=True)
    date_inserted = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')
    objects = UsersManager()

    USERNAME_FIELD = 'email'

    def is_admin(self):
        return self.user_id == 1

    def has_role(self, role: str):
        return self.role == Roles.objects.get(name=role)

    @property
    def dashboard(self):
        """Returns the dashboard url for the user
        Returns an empty string if the user has no role"""
        if self.is_admin():
            role = 'Admin'
        else:
            role = self.role
        if role is not None:
            return str(role).lower() + '_dashboard'
        else:
            return ''

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.name

    class Meta:
        managed = True


class Clubs(models.Model):
    club = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    accepting_members = models.BooleanField()
    image = models.URLField(blank=True, null=True) 
    date_inserted = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def members(self):
        return [Users.objects.get(user_id=relationship.user_id) for relationship in
                ClubMembers.objects.filter(club_id=self.club_id).all()]

    def __str__(self):
        return self.name


class ClubMembers(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    club = models.ForeignKey(Clubs, on_delete=models.CASCADE)
    date_inserted = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"User: {self.user}, Club: {self.club}"


class ClubRequests(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    club = models.ForeignKey(Clubs, on_delete=models.CASCADE)
    date_inserted = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"User: {self.user}, Club: {self.club}"


class AccountRequests(models.Model):
    a_request_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)
    password = models.CharField(max_length=128)
    contact_details = models.CharField(max_length=255, blank=True, null=True)
    date_inserted = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.email
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)


class Events(models.Model):
    event_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    club = models.ForeignKey(Clubs, on_delete=models.CASCADE)
    event_time = models.DateTimeField()
    venue = models.CharField(max_length=255)
    date_inserted = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"Title: {self.title}"


class EventRequests(models.Model):
    event = models.ForeignKey('Events', models.DO_NOTHING)
    user = models.ForeignKey(Users, models.DO_NOTHING)
    date_inserted = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)


class EventMembers(models.Model):
    event = models.ForeignKey('Events', models.DO_NOTHING)
    user = models.ForeignKey(Users, models.DO_NOTHING)
    date_inserted = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

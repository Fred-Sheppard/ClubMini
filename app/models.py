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
class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)  # Set on_delete behavior
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    contact_details = models.CharField(max_length=255, blank=True, null=True)
    date_inserted = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name


# AccountRequests Model
class AccountRequests(models.Model):
    a_request_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=255, unique=True)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)  # Set on_delete behavior
    date_inserted = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.email


# Clubs Model
class Clubs(models.Model):
    club = models.OneToOneField(Users, on_delete=models.CASCADE, primary_key=True)  # Use user_id as PK
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    accepting_members = models.BooleanField()
    image = models.BinaryField(blank=True, null=True)
    date_inserted = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)

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

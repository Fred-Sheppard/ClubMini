# Generated by Django 5.0.2 on 2024-02-22 15:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Users",
            fields=[
                ("user_id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("email", models.CharField(max_length=255, unique=True)),
                ("password", models.CharField(max_length=255)),
                (
                    "contact_details",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("date_inserted", models.DateTimeField(auto_now_add=True, null=True)),
                ("date_updated", models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Events",
            fields=[
                ("event_id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=255)),
                (
                    "description",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("event_time", models.DateTimeField()),
                ("venue", models.CharField(max_length=255)),
                ("date_inserted", models.DateTimeField(auto_now_add=True, null=True)),
                ("date_updated", models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Roles",
            fields=[
                ("role_id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("date_inserted", models.DateTimeField(auto_now_add=True, null=True)),
                ("date_updated", models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Clubs",
            fields=[
                (
                    "club",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="app.users",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.CharField(max_length=255)),
                ("accepting_members", models.BooleanField()),
                ("image", models.BinaryField(blank=True, null=True)),
                ("date_inserted", models.DateTimeField(auto_now_add=True, null=True)),
                ("date_updated", models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="EventRequests",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_inserted", models.DateTimeField(auto_now_add=True, null=True)),
                ("date_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to="app.users"
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING, to="app.events"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="users",
            name="role",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="app.roles"
            ),
        ),
        migrations.CreateModel(
            name="AccountRequests",
            fields=[
                ("a_request_id", models.AutoField(primary_key=True, serialize=False)),
                ("email", models.CharField(max_length=255, unique=True)),
                ("date_inserted", models.DateTimeField(auto_now_add=True, null=True)),
                ("date_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "role",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.roles"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="events",
            name="club",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="app.clubs"
            ),
        ),
        migrations.CreateModel(
            name="ClubRequests",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_inserted", models.DateTimeField(auto_now_add=True, null=True)),
                ("date_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.users"
                    ),
                ),
                (
                    "club",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.clubs"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ClubMembers",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_inserted", models.DateTimeField(auto_now_add=True, null=True)),
                ("date_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.users"
                    ),
                ),
                (
                    "club",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.clubs"
                    ),
                ),
            ],
        ),
    ]
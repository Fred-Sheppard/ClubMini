# Generated by Django 5.0.2 on 2024-02-24 16:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Users",
            fields=[
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                ("user_id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("email", models.CharField(max_length=255, unique=True)),
                ("password", models.CharField(max_length=128)),
                (
                    "contact_details",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("date_inserted", models.DateTimeField(auto_now_add=True, null=True)),
                ("date_updated", models.DateTimeField(auto_now=True, null=True)),
                (
                    "group",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="auth.group",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        related_name="custom_user_permissions", to="auth.permission"
                    ),
                ),
            ],
            options={
                "managed": True,
            },
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
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("description", models.CharField(max_length=255)),
                ("accepting_members", models.BooleanField()),
                ("image", models.TextField(null=True)),
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
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
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
            model_name="users",
            name="role",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="app.roles"
            ),
        ),
        migrations.AddField(
            model_name="events",
            name="club",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="app.clubs"
            ),
        ),
        migrations.AddField(
            model_name="clubs",
            name="members",
            field=models.ManyToManyField(
                related_name="members", to=settings.AUTH_USER_MODEL
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
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
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
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
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

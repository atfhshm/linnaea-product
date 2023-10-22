# Generated by Django 4.2.6 on 2023-10-22 07:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_user_role"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="username",
        ),
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("ORG_ADMIN", "Organization admin"),
                    ("ORG_MANAGER", "Organization managers"),
                    ("ORG_MEMBERS", "Organization member"),
                    ("INTERNAL", "Internal"),
                ],
                default="INTERNAL",
                max_length=20,
                verbose_name="role",
            ),
        ),
    ]

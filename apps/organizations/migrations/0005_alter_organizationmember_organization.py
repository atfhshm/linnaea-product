# Generated by Django 4.2.6 on 2023-10-22 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("organizations", "0004_organizationmember"),
    ]

    operations = [
        migrations.AlterField(
            model_name="organizationmember",
            name="organization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="org_members",
                to="organizations.organization",
            ),
        ),
    ]

# Generated by Django 4.0.6 on 2022-10-02 11:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_alter_profile_created"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="name",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]

# Generated by Django 4.0.6 on 2022-10-02 11:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0008_alter_profile_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="name",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]

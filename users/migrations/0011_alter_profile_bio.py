# Generated by Django 4.2.2 on 2023-06-28 19:27

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0010_alter_profile_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="bio",
            field=ckeditor.fields.RichTextField(),
        ),
    ]
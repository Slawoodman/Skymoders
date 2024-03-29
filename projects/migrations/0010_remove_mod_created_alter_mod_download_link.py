# Generated by Django 4.2.1 on 2023-05-29 23:27

from django.db import migrations, models
import projects.models


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0009_alter_mod_featured_image"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="mod",
            name="created",
        ),
        migrations.AlterField(
            model_name="mod",
            name="download_link",
            field=models.FileField(
                upload_to="files/", validators=[projects.models.validation_file]
            ),
        ),
    ]

# Generated by Django 4.0.6 on 2022-10-11 12:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0008_gallery_user_owner"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mod",
            name="featured_image",
            field=models.ImageField(
                blank=True, default="default.png", null=True, upload_to="modtitle/"
            ),
        ),
    ]

# Generated by Django 4.2.2 on 2023-08-04 16:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0020_gallery_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gallery",
            name="title",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
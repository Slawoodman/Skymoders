# Generated by Django 4.2.2 on 2023-07-26 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0013_mod_view_count"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mod",
            name="view_count",
            field=models.PositiveIntegerField(default=1),
        ),
    ]
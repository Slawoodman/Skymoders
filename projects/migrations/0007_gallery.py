# Generated by Django 4.0.6 on 2022-10-07 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("projects", "0006_alter_mod_owner"),
    ]

    operations = [
        migrations.CreateModel(
            name="Gallery",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "img",
                    models.ImageField(blank=True, null=True, upload_to="modgallery/"),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="projects.mod",
                    ),
                ),
            ],
        ),
    ]

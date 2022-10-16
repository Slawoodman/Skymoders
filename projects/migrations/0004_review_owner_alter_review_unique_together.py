# Generated by Django 4.1 on 2022-09-09 21:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_profile_options_alter_profile_created"),
        ("projects", "0003_alter_mod_options_alter_mod_created"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="users.profile",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="review",
            unique_together={("owner", "mod")},
        ),
    ]
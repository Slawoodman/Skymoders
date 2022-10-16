# Generated by Django 4.0.6 on 2022-10-07 22:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_profile_name'),
        ('projects', '0007_gallery'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery',
            name='user_owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
    ]
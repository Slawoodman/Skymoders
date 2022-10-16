# Generated by Django 4.0.6 on 2022-10-01 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_message_options'),
        ('projects', '0005_alter_mod_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mod',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
    ]
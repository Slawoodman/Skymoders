# Generated by Django 4.0.6 on 2023-06-25 14:06

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0011_rename_download_link_mod_modfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mod',
            name='description',
            field=ckeditor.fields.RichTextField(),
        ),
    ]

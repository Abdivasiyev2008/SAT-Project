# Generated by Django 4.2 on 2025-02-04 07:03

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('module_4', '0005_time4'),
    ]

    operations = [
        migrations.AddField(
            model_name='module_4_question',
            name='explanation',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]

# Generated by Django 4.2 on 2025-01-08 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificate', '0010_alter_certificate_english_alter_certificate_math_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certificate',
            name='english',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='math',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='certificate',
            name='overall',
            field=models.IntegerField(default=0),
        ),
    ]

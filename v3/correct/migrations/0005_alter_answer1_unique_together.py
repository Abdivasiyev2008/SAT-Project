# Generated by Django 4.2 on 2025-01-28 13:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('correct', '0004_alter_answer1_correct_answer_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='answer1',
            unique_together=set(),
        ),
    ]

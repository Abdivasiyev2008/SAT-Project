# Generated by Django 4.2 on 2025-01-29 14:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('correct', '0010_module4_ans_module3_ans_module2_ans_answer4_answer3_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer1',
            name='question',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='answer2',
            name='question',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='answer3',
            name='question',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='answer4',
            name='question',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]

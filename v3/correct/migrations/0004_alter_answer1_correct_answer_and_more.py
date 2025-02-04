# Generated by Django 4.2 on 2025-01-28 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('correct', '0003_alter_answer1_correct_answer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer1',
            name='correct_answer',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='answer1',
            name='module1_ans',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='correct.module1_ans'),
        ),
        migrations.AlterField(
            model_name='answer1',
            name='module1_user_ans',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='answer1',
            unique_together={('module1_ans', 'module1_user_ans', 'correct_answer')},
        ),
    ]

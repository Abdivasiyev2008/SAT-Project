# Generated by Django 4.2 on 2025-01-07 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module_4', '0003_alter_module_4_question_option_a_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='module_4_question',
            name='term',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]

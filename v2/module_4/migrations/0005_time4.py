# Generated by Django 4.2 on 2025-01-26 21:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0005_hidepractice_hideuser_practice_action_practice_image_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('module_4', '0004_alter_module_4_question_term'),
    ]

    operations = [
        migrations.CreateModel(
            name='Time4',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.IntegerField(default=1920)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('practice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.practice')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

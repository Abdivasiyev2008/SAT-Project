# Generated by Django 4.2 on 2024-12-17 15:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tests', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('english', models.IntegerField()),
                ('math', models.IntegerField()),
                ('overall', models.IntegerField()),
                ('time', models.DateTimeField(auto_now=True)),
                ('practice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tests.practice')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
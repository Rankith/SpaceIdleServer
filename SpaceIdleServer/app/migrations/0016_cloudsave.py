# Generated by Django 3.2.15 on 2022-10-26 00:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0015_auto_20221025_1734'),
    ]

    operations = [
        migrations.CreateModel(
            name='CloudSave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('save_data', models.TextField()),
                ('total_playtime', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

# Generated by Django 2.2.28 on 2022-09-14 02:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_player_highest_sector'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='player_id',
            new_name='player_uuid',
        ),
    ]

# Generated by Django 2.2.28 on 2022-09-14 00:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_id', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(choices=[('SectorCleared', 'SectorCleared'), ('RecipeUnlock', 'RecipeUnlock'), ('ModuleUnlock', 'ModuleUnlock'), ('AchievementComplete', 'AchievementComplete'), ('ResearchComplete', 'ResearchComplete'), ('Unlock', 'Unlock'), ('AIUpgrade', 'AIUpgrade'), ('GameOpened', 'GameOpened')], max_length=50)),
                ('details', models.CharField(max_length=255)),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.Player')),
            ],
        ),
    ]
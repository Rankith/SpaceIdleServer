from django.db import models

# Create your models here.
class Player(models.Model):
    player_uuid = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(blank=True)
    highest_sector = models.IntegerField(default=1)
    nick_name = models.CharField(max_length=255,blank=True,default='')
    def __str__(self):
        return str(self.player_uuid)


class Activity(models.Model):
    player = models.ForeignKey(Player, on_delete=models.SET_NULL,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    ACTIVITY_TYPES = (
        ('SectorCleared','SectorCleared'),
        ('RecipeUnlock','RecipeUnlock'),
        ('ModuleUnlock','ModuleUnlock'),
        ('AchievementComplete','AchievementComplete'),
        ('ResearchComplete','ResearchComplete'),
        ('Unlock','Unlock'),
        ('AIUpgrade','AIUpgrade'),
        ('GameOpened','GameOpened'),
        ('ShardCompleted','ShardCompleted'),
        ('InfiniteResource','InfiniteResource'),
        ('PrestigeReset','PrestigeReset'),
        ('RedeemCode','RedeemCode'),
        )
    type = models.CharField(max_length=50,choices=ACTIVITY_TYPES)
    details = models.CharField(max_length=255)
    details2 = models.CharField(max_length=255,blank=True,default='')

class Code(models.Model):
    code = models.CharField(max_length=255)
    date_start = models.DateTimeField(blank=True,null=True)
    date_end = models.DateTimeField(blank=True,null=True)
    reward = models.TextField()

class CloudSave(models.Model):
    player = models.ForeignKey(Player, on_delete=models.SET_NULL,null=True)
    save_data = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)
from django.contrib import admin
from app.models import *
# Register your models here.

class PlayerAdmin(admin.ModelAdmin):
    list_display=('id','player_uuid','nick_name','account','date_created','last_updated','highest_sector')

class ActivityAdmin(admin.ModelAdmin):
    readonly_fields = ('date_created',)
    list_display=('id','player','type','details','details2','date_created')
    list_editable=('type','details')
    list_filter=('type',)
    search_fields=('player__player_uuid','player__nick_name')

class CodeAdmin(admin.ModelAdmin):
    list_display=('id','code','date_start','date_end','reward')
    list_editable=('code','date_start','date_end','reward')

class CloudSaveAdmin(admin.ModelAdmin):
    readonly_fields = ('timestamp',)
    list_display=('id','account','timestamp')

class CloudSaveOLDAdmin(admin.ModelAdmin):
    list_display=('id','player','save_data')


admin.site.register(Player,PlayerAdmin)
admin.site.register(Activity,ActivityAdmin)
admin.site.register(Code,CodeAdmin)
admin.site.register(CloudSave,CloudSaveAdmin)
admin.site.register(CloudSaveOLD,CloudSaveOLDAdmin)
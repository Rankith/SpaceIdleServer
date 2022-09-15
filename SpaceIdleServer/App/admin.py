from django.contrib import admin
from app.models import *
# Register your models here.

class PlayerAdmin(admin.ModelAdmin):
    list_display=('id','player_uuid','date_created','last_updated','highest_sector')

class ActivityAdmin(admin.ModelAdmin):
    readonly_fields = ('date_created',)
    list_display=('id','player','type','details','date_created')
    list_editable=('type','details')
    list_filter=('type',)


admin.site.register(Player,PlayerAdmin)
admin.site.register(Activity,ActivityAdmin)
from django.shortcuts import render
from datetime import datetime
from app.models import *
from django.db.models import Q
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
@csrf_exempt
def activity_log(request):
    data = json.loads(request.body.decode("utf-8"))

    #lookup player
    player = Player.objects.filter(player_uuid=data['player_uuid']).first()
    if player == None:
        #doesnt exist, make one
        player = Player(player_uuid=data['player_uuid'],last_updated=datetime.now())
        player.save()
    else:
        player.last_updated = datetime.now()
        player.save()

    activity = Activity(player=player,type=data['type'],details=data['details'],details2=data['details2'])
    activity.save()

    if data['type'] == 'SectorCleared':
        player.highest_sector = int(data['details2'])
        player.save()


    return HttpResponse(status=200)
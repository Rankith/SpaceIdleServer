from django.shortcuts import render
from datetime import datetime
from app.models import *
from django.db.models import Q
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
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

    #check for this activity and delete if pure duplicate exists
    Activity.objects.filter(player=player,type=data['type'],details=data['details'],details2=data['details2']).delete()
    activity = Activity(player=player,type=data['type'],details=data['details'],details2=data['details2'])
    activity.save()

    if data['type'] == 'SectorCleared':
        player.highest_sector = int(data['details2'])
        player.save()


    return HttpResponse(status=200)

@csrf_exempt
def enter_code(request):
    data = json.loads(request.body.decode("utf-8"))
    code_in = data['code']

    valid = True

    code = Code.objects.filter(code=code_in).first()
    if code != None:
        if code.date_start != None:
            if code.date_start > timezone.now():
                valid = False
        if code.date_end != None:
            if code.date_end < timezone.now():
                valid = False
    else:
        valid = False

    if valid:
        #log redemption
        #lookup player
        player = Player.objects.filter(player_uuid=data['player_uuid']).first()
        if player == None:
            #doesnt exist, make one
            player = Player(player_uuid=data['player_uuid'],last_updated=datetime.now())
            player.save()
        else:
            player.last_updated = datetime.now()
            player.save()

        #check for this activity and delete if pure duplicate exists
        activity = Activity(player=player,type='RedeemCode',details=code_in,details2='')
        activity.save()
        return JsonResponse(json.loads(code.reward))
    else:
         return HttpResponse(status=400)
     

@csrf_exempt
def cloud_save(request):
    data = json.loads(request.body.decode("utf-8"))

    #lookup player
    player = Player.objects.filter(player_uuid=data['player_uuid']).first()
    if player == None:
        #doesnt exist, make one
        player = Player(player_uuid=data['player_uuid'],last_updated=datetime.now())
        player.save()

    #lookup cloud save
    cs = CloudSave.objects.filter(player=player).first()
    if cs == None:
        cs = CloudSave(player=player,save_data=data['save_data'])
    else:
        cs.save_data= data['save_data']
    cs.save()

    return HttpResponse(status=200)
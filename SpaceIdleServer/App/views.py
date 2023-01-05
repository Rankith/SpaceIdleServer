from django.shortcuts import render
from datetime import datetime, timedelta
from app.models import *
from django.db.models import Q, F, Func, ExpressionWrapper, DurationField, Aggregate, FloatField, Avg, IntegerField, Count
from django.db.models.functions import Cast
import json
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
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
    #check if already exists
    kwargs = {'username': data['username']}
    try:
        user = get_user_model().objects.get(**kwargs)
        if user.check_password(data['password']):
            #save it
            cs = CloudSave.objects.filter(account=user).first()
            if cs == None:
                cs = CloudSave(account=user,save_data=data['save_data'],total_playtime=data['total_playtime'])
            else:
                cs.save_data= data['save_data']
                cs.total_playtime= data['total_playtime']
            cs.save()
            return HttpResponse(status=200)
    except:
        pass

    return HttpResponse(status=404)

@csrf_exempt
def get_cloud_save(request):
    data = json.loads(request.body.decode("utf-8"))
    #check if already exists
    kwargs = {'username': data['username']}
    try:
        user = get_user_model().objects.get(**kwargs)
        if user.check_password(data['password']):
            #grab save
            cs = CloudSave.objects.filter(account=user).first()
            return JsonResponse({"save_data":cs.save_data,"total_playtime":cs.total_playtime,"timestamp":cs.timestamp})
    except:
        pass

    return HttpResponse(status=404)

@csrf_exempt
def cloud_register(request):
    data = json.loads(request.body.decode("utf-8"))
    #check if already exists
    if User.objects.filter(username=data['username']).first() != None:
        return JsonResponse({"result":"User Already Exists"})

    new_user = User.objects.create_user(username=data['username'],password=data['password'])
    new_user.save()

    #attach account just for looking up later
    player = Player.objects.filter(player_uuid=data['player_uuid']).first()
    if player == None:
        #doesnt exist, make one
        player = Player(player_uuid=data['player_uuid'],last_updated=datetime.now(),account=user)
        player.save()
    else:
        player.last_updated = datetime.now()
        player.account = new_user
        player.save()

    return JsonResponse({"result":"Account Created"})

@csrf_exempt
def cloud_login(request):
    data = json.loads(request.body.decode("utf-8"))
    #check if already exists
    kwargs = {'username': data['username']}
    try:
        user = get_user_model().objects.get(**kwargs)
        if user.check_password(data['password']):
            #now get the user id
            player = Player.objects.filter(account=user).first()
            return JsonResponse({"result":"Success","uuid":player.player_uuid})   
        else:
            return JsonResponse({"result":"Invalid Password"})   
    except:
        return JsonResponse({"result":"Invalid Username"})

    return JsonResponse({"result":"Unknown Error"})

def progress_graph(request):
    date_filter = request.GET.get('date_start','2022-06-01')
    stats = Activity.objects.filter(type='SectorCleared',player__date_created__gte=date_filter).exclude(player__player_uuid='909dcb16-bfb7-4f2d-9519-1ccec46bcd38').annotate(details_int=Cast('details2',IntegerField())).values('details2').order_by('details_int').annotate(time_taken=Avg(ExpressionWrapper(F('date_created')-F('player__date_created'),output_field=DurationField())))
    labels = []
    values = []
    index = 0
    for s in stats:
        labels.append(s['details2'])
        values.append(round(s['time_taken'].total_seconds()/60/60,2))
    # unpack dict keys / values into two lists
    #labels, values = zip(*stats)

    context = {
        "labels": labels,
        "values": values,
    }
    return render(request, "app/progress_graph.html", context)

#sector abandaoned
def abandon_graph(request):
    days_stagnant = request.GET.get('days_stagnant','15')
    date_start = request.GET.get('date_start','2022-06-01')
    date_compare = datetime.now() + timedelta(days=-int(days_stagnant))
    stats = Player.objects.filter(last_updated__lte=date_compare,date_created__gte=date_start).exclude(highest_sector=1).exclude(player_uuid='909dcb16-bfb7-4f2d-9519-1ccec46bcd38').values('highest_sector').order_by('highest_sector').annotate(amount=Count('highest_sector'))
    labels = []
    values = []
    index = 0
    for s in stats:
        labels.append(s['highest_sector'])
        values.append(s['amount'])
    # unpack dict keys / values into two lists
    #labels, values = zip(*stats)

    context = {
        "labels": labels,
        "values": values,
    }
    return render(request, "app/abandon_graph.html", context)

class Median(Aggregate):
        function = 'PERCENTILE_CONT'
        name = 'median'
        output_field = FloatField()
        template = '%(function)s(0.5) WITHIN GROUP (ORDER BY %(expressions)s)'
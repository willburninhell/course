from django.shortcuts import render, HttpResponse
from .models import *
from ABNS.include.ping import do_one
import datetime


def monitor(request):
    groups_results = {}
    groups_query = Group.objects.all().order_by('name')
    cp_query = ControlPoint.objects.all().order_by('group', 'name')
    alarm_query_down = Alarm.objects.filter(up__isnull=True).order_by('down').reverse()
    alarm_query_up = Alarm.objects.filter(up__isnull=False, down__gt=datetime.datetime.now() - datetime.timedelta(days=7)).order_by('down').reverse()
    alarm = False
    cp_ping = {}
    for group in groups_query:
        groups_results[group.name] = [0, 0]
    for cp in cp_query:
        cp_ping[cp.name] = do_one(cp.ip, 0.1) > 0
        if cp_ping[cp.name]:
            alarms = Alarm.objects.filter(control_point=cp, up__isnull=True)
            if len(alarms) > 0:
                a = alarms[0]
                a.up = datetime.datetime.now()
                a.save()
                print cp.name, 'up!'
                alarm = True
            groups_results[cp.group.name][0] += 1
        else:
            groups_results[cp.group.name][1] += 1
            alarms = Alarm.objects.filter(control_point=cp)
            if len(alarms) > 0:
                if len(alarms.filter(up__isnull=True)) == 0:
                    a = Alarm(control_point=cp)
                    a.save()
                    print('added', cp.name)
                    alarm = True
            else:
                a = Alarm(control_point=cp)
                a.save()
                print('added', cp.name)
                alarm = True

    return render(request, "monitor.html", {'groups_query': groups_query,
                                            'groups_results': groups_results,
                                            'alarm_query_up': alarm_query_up,
                                            'alarm_query_down': alarm_query_down,
                                            'alarm': alarm})


def alarm_info(request, id):
    postdata = request.GET
    print postdata
    if postdata != {}:
        a = Alarm.objects.get(id=id)
        a.comment = postdata['comment']
        a.save(update_fields=['comment'])
        return HttpResponse(status=200)
    alarm = Alarm.objects.get(pk=id)

    return render(request, "alarm.html", {'alarm': alarm})

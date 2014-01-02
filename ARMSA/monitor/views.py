from django.shortcuts import render, HttpResponse
from .models import *
from ABNS.include.ping import do_one
import datetime


def update(request=None):
    print('ololo!')
    cp_query = ControlPoint.objects.all().order_by('group', 'name')
    cp_ping = {}
    for cp in cp_query:
        cp_ping[cp.name] = do_one(cp.ip, 0.05) > 0
        if cp_ping[cp.name]:
            alarms = Alarm.objects.filter(control_point=cp, up__isnull=True)
            if len(alarms) > 0:
                a = alarms[0]
                a.up = datetime.datetime.now()
                a.shown = False
                a.save()
        else:
            alarms = Alarm.objects.filter(control_point=cp)
            if len(alarms) > 0:
                if len(alarms.filter(up__isnull=True)) == 0:
                    a = Alarm(control_point=cp)
                    a.save()
            else:
                a = Alarm(control_point=cp)
                a.save()
    return HttpResponse(status=200)


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
        al = Alarm.objects.filter(control_point=cp)
        if len(al) > 0:
            if al.latest('id').up is None:
                cp_ping[cp.name] = False
            else:
                cp_ping[cp.name] = True
        else:
            cp_ping[cp.name] = True
        if cp_ping[cp.name]:
            groups_results[cp.group.name][0] += 1
        else:
            groups_results[cp.group.name][1] += 1
    if len(Alarm.objects.filter(shown=False)) > 0:
        alarm = True
        for al in Alarm.objects.filter(shown=False):
            al.shown = True
            al.save()


    return render(request, "monitor.html", {'groups_query': groups_query,
                                            'groups_results': groups_results,
                                            'alarm_query_up': alarm_query_up,
                                            'alarm_query_down': alarm_query_down,
                                            'alarm': alarm})


def show_group(request, gr = 1):
    group = Group.objects.get(id=gr)
    cp_query = ControlPoint.objects.filter(group=group)
    alarm_query_down = Alarm.objects.filter(control_point__group=group, up__isnull=True).order_by('down').reverse()
    alarm_query_up = Alarm.objects.filter(control_point__group=group, up__isnull=False, down__gt=datetime.datetime.now() - datetime.timedelta(days=7)).order_by('down').reverse()
    alarm = False
    cp_ping = {}
    for cp in cp_query:
        al = Alarm.objects.filter(control_point=cp)
        if len(al) > 0:
            if al.latest('id').up is None:
                cp_ping[cp.name] = False
            else:
                cp_ping[cp.name] = True
        else:
            cp_ping[cp.name] = True
    if len(Alarm.objects.filter(shown=False)) > 0:
        alarm = True
        for al in Alarm.objects.filter(shown=False):
            al.shown = True
            al.save()
    return render(request, 'showgroup.html', {'group': group,
                                              'cp_query': cp_query,
                                              'cp_ping': cp_ping,
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

from django.shortcuts import render, HttpResponse
from .models import *
from ABNS.include.ping import do_one
import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader, Context


def sendmail(request=None):
    t = loader.get_template('mail_template.txt')
    end_date = datetime.date.today()
    start_date = datetime.date.today() + relativedelta(days=-6)
    alarms = Alarm.objects.filter(down__gt=datetime.datetime.combine(start_date, datetime.time.min),
                                  down__lt=datetime.datetime.combine(end_date, datetime.time.max)).order_by('control_point__group','control_point','down').reverse()
    # downtime = datetime.timedelta(0)
    # for al in alarms:
    #     if al.up is None:
    #         downtime += ((now + relativedelta(hours=-2))-al.down)
    #     else:
    #         downtime += (al.up-al.down)
    # secs = downtime.total_seconds()
    # down = 100*downtime.total_seconds()/(
    #     (((now.weekday()*24)+now.hour)*60+now.minute)*60+now.second)
    # up = 100 - down
    # counter = len(alarms)
    # downtime = downtime - datetime.timedelta(microseconds=downtime.microseconds)

    c = Context({
        'end_date': end_date,
        'start_date': start_date,
        'alarms': alarms,
        })
    send_mail('Subject here', t.render(c), settings.EMAIL_HOST_USER, ['willburninhell@gmail.com'], fail_silently=False)
    return HttpResponse(status=200)


def update(request=None):
    print('ololo!')
    print timezone.now()
    print datetime.datetime.now()
    cp_query = ControlPoint.objects.all().order_by('group', 'name')
    cp_ping = {}
    for cp in cp_query:
        cp_ping[cp.name] = do_one(cp.ip, 0.05) > 0
        if cp_ping[cp.name]:
            alarms = Alarm.objects.filter(control_point=cp, up__isnull=True)
            if len(alarms) > 0:
                a = alarms[0]
                a.up = timezone.now()
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
    alarm_query_down = Alarm.objects.filter(
        up__isnull=True).order_by('down').reverse()
    alarm_query_up = Alarm.objects.filter(
        up__isnull=False,
        down__gt=timezone.now() - datetime.timedelta(
            days=7)).order_by('down').reverse()
    alarm = False
    cp_ping = {}
    total_up = 0
    total_down = 0
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
            total_up += 1
        else:
            groups_results[cp.group.name][1] += 1
            total_down += 1
    if len(Alarm.objects.filter(shown=False)) > 0:
        alarm = True
        for al in Alarm.objects.filter(shown=False):
            al.shown = True
            al.save()

    return render(request, "monitor.html", {
        'groups_query': groups_query,
        'groups_results': groups_results,
        'alarm_query_up': alarm_query_up,
        'alarm_query_down': alarm_query_down,
        'total_up': total_up,
        'total_down': total_down,
        'alarm': alarm})


def show_group(request, gr=1):
    group = Group.objects.get(id=gr)
    cp_query = ControlPoint.objects.filter(group=group)
    alarm_query_down = Alarm.objects.filter(
        control_point__group=group,
        up__isnull=True).order_by('down').reverse()
    alarm_query_up = Alarm.objects.filter(
        control_point__group=group,
        up__isnull=False,
        down__gt=timezone.now() - datetime.timedelta(
            days=7)).order_by('down').reverse()
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
    return render(request, 'showgroup.html', {
        'group': group,
        'cp_query': cp_query,
        'cp_ping': cp_ping,
        'alarm_query_up': alarm_query_up,
        'alarm_query_down': alarm_query_down,
        'alarm': alarm})


def show_cp(request, cp=1):
    cpoint = ControlPoint.objects.get(id=cp)
    info = {}
    info['today'] = {}
    info['yesterday'] = {}
    info['thisweek'] = {}
    info['lastweek'] = {}
    info['thismonth'] = {}
    info['lastmonth'] = {}
    info['thisyear'] = {}
    info['lastyear'] = {}

    now = timezone.now() + relativedelta(hours=2)
    today = datetime.datetime(now.year, now.month, now.day, 0, 0, 0, 0) + relativedelta(hours=2)
    yesterday = today + relativedelta(days=-1) + relativedelta(hours=2)
    thisweek = today + relativedelta(days=-(now.weekday())) + relativedelta(hours=2)
    lastweek = thisweek + relativedelta(weeks=-1) + relativedelta(hours=2)
    thismonth = datetime.datetime(now.year, now.month, 1, 0, 0, 0, 0) + relativedelta(hours=2)
    lastmonth = thismonth + relativedelta(months=-1) + relativedelta(hours=2)
    thisyear = datetime.datetime(now.year, 1, 1, 0, 0, 0, 0) + relativedelta(hours=2)
    lastyear = thisyear + relativedelta(years=-1) + relativedelta(hours=2)
    # today
    alarms = Alarm.objects.filter(control_point=cpoint,
                                  down__gt=today).order_by('down').reverse()
    info['today']['downtime'] = 0
    info['today']['up'] = 0
    info['today']['down'] = 0
    info['today']['times'] = 0
    downtime = datetime.timedelta(0)
    for al in alarms:
        if al.up is None:
            downtime += ((now + relativedelta(hours=-2))-al.down)
        else:
            downtime += (al.up-al.down)
    secs = downtime.total_seconds()
    down = 100*downtime.total_seconds()/(
        (now.hour*60+now.minute)*60+now.second)
    up = 100 - down
    counter = len(alarms)
    downtime = downtime - datetime.timedelta(microseconds=downtime.microseconds)
    print 'today', secs, down, up, counter
    info['today']['downtime'] = downtime
    info['today']['up'] = up
    info['today']['down'] = down
    info['today']['times'] = counter
    #yesterday
    alarms = Alarm.objects.filter(control_point=cpoint,
                                  down__gt=yesterday,
                                  down__lt=today).order_by('down').reverse()
    info['yesterday']['downtime'] = 0
    info['yesterday']['up'] = 0
    info['yesterday']['down'] = 0
    info['yesterday']['times'] = 0
    downtime = datetime.timedelta(0)
    for al in alarms:
        if (al.up - today) > 0:
            downtime += (today-al.down)
        else:
            downtime += (al.up-al.down)
    secs = downtime.total_seconds()
    down = 100*downtime.total_seconds()/(today - yesterday).total_seconds()
    up = 100 - down
    counter = len(alarms)
    downtime = downtime - datetime.timedelta(microseconds=downtime.microseconds)
    print 'yesterday', secs, down, up, counter
    info['yesterday']['downtime'] = downtime
    info['yesterday']['up'] = up
    info['yesterday']['down'] = down
    info['yesterday']['times'] = counter
    #this week
    alarms = Alarm.objects.filter(control_point=cpoint,
                                  down__gt=thisweek).order_by('down').reverse()
    info['thisweek']['downtime'] = 0
    info['thisweek']['up'] = 0
    info['thisweek']['down'] = 0
    info['thisweek']['times'] = 0
    downtime = datetime.timedelta(0)
    for al in alarms:
        if al.up is None:
            downtime += ((now + relativedelta(hours=-2))-al.down)
        else:
            downtime += (al.up-al.down)
    secs = downtime.total_seconds()
    down = 100*downtime.total_seconds()/(
        (((now.weekday()*24)+now.hour)*60+now.minute)*60+now.second)
    up = 100 - down
    counter = len(alarms)
    downtime = downtime - datetime.timedelta(microseconds=downtime.microseconds)
    print 'this week', secs, down, up, counter
    info['thisweek']['downtime'] = downtime
    info['thisweek']['up'] = up
    info['thisweek']['down'] = down
    info['thisweek']['times'] = counter
    #last week
    alarms = Alarm.objects.filter(control_point=cpoint,
                                  down__gt=lastweek,
                                  down__lt=thisweek).order_by('down').reverse()
    info['lastweek']['downtime'] = 0
    info['lastweek']['up'] = 0
    info['lastweek']['down'] = 0
    info['lastweek']['times'] = 0
    downtime = datetime.timedelta(0)
    for al in alarms:
        if (al.up - thisweek) > 0:
            downtime += (thisweek-al.down)
        else:
            downtime += (al.up-al.down)
    secs = downtime.total_seconds()
    down = 100*downtime.total_seconds()/(thisweek - lastweek).total_seconds()
    up = 100 - down
    counter = len(alarms)
    downtime = downtime - datetime.timedelta(microseconds=downtime.microseconds)
    print 'last week', secs, down, up, counter
    info['lastweek']['downtime'] = downtime
    info['lastweek']['up'] = up
    info['lastweek']['down'] = down
    info['lastweek']['times'] = counter
    #this month
    alarms = Alarm.objects.filter(
        control_point=cpoint,
        down__gt=thismonth).order_by('down').reverse()
    info['thismonth']['downtime'] = 0
    info['thismonth']['up'] = 0
    info['thismonth']['down'] = 0
    info['thismonth']['times'] = 0
    downtime = datetime.timedelta(0)
    for al in alarms:
        if al.up is None:
            downtime += ((now + relativedelta(hours=-2))-al.down)
        else:
            downtime += (al.up-al.down)
    secs = downtime.total_seconds()
    down = 100*downtime.total_seconds()/(
        ((((now.day-1)*24)+now.hour)*60+now.minute)*60+now.second)
    up = 100 - down
    counter = len(alarms)
    downtime = downtime - datetime.timedelta(microseconds=downtime.microseconds)
    print 'this month', secs, down, up, counter
    info['thismonth']['downtime'] = downtime
    info['thismonth']['up'] = up
    info['thismonth']['down'] = down
    info['thismonth']['times'] = counter
    #last month
    alarms = Alarm.objects.filter(
        control_point=cpoint,
        down__gt=lastmonth,
        down__lt=thismonth).order_by('down').reverse()
    info['lastmonth']['downtime'] = 0
    info['lastmonth']['up'] = 0
    info['lastmonth']['down'] = 0
    info['lastmonth']['times'] = 0
    downtime = datetime.timedelta(0)
    for al in alarms:
        if (al.up - thismonth) > 0:
            downtime += (thismonth-al.down)
        else:
            downtime += (al.up-al.down)
    secs = downtime.total_seconds()
    down = 100*downtime.total_seconds()/(thismonth - lastmonth).total_seconds()
    up = 100 - down
    counter = len(alarms)
    downtime = downtime - datetime.timedelta(microseconds=downtime.microseconds)
    print 'last month', secs, down, up, counter
    info['lastmonth']['downtime'] = downtime
    info['lastmonth']['up'] = up
    info['lastmonth']['down'] = down
    info['lastmonth']['times'] = counter
    #this year
    alarms = Alarm.objects.filter(control_point=cpoint,
                                  down__gt=thisyear).order_by('down').reverse()
    info['thisyear']['downtime'] = 0
    info['thisyear']['up'] = 0
    info['thisyear']['down'] = 0
    info['thisyear']['times'] = 0
    downtime = datetime.timedelta(0)
    for al in alarms:
        if al.up is None:
            downtime += ((now + relativedelta(hours=-2))-al.down)
        else:
            downtime += (al.up-al.down)
    secs = downtime.total_seconds()
    down = 100*downtime.total_seconds()/(((((
        now.timetuple().tm_yday-1)*24)+now.hour)*60+now.minute)*60+now.second)
    up = 100 - down
    counter = len(alarms)
    downtime = downtime - datetime.timedelta(microseconds=downtime.microseconds)
    print 'this year', secs, down, up, counter
    info['thisyear']['downtime'] = downtime
    info['thisyear']['up'] = up
    info['thisyear']['down'] = down
    info['thisyear']['times'] = counter
    #last year
    alarms = Alarm.objects.filter(control_point=cpoint,
                                  down__gt=lastyear,
                                  down__lt=thisyear).order_by('down').reverse()
    info['lastyear']['downtime'] = 0
    info['lastyear']['up'] = 0
    info['lastyear']['down'] = 0
    info['lastyear']['times'] = 0
    downtime = datetime.timedelta(0)
    for al in alarms:
        if (al.up - thisyear) > 0:
            downtime += (thisyear-al.down)
        else:
            downtime += (al.up-al.down)
    secs = downtime.total_seconds()
    down = 100*downtime.total_seconds()/(thisyear - lastyear).total_seconds()
    up = 100 - down
    counter = len(alarms)
    downtime = downtime - datetime.timedelta(microseconds=downtime.microseconds)
    print 'last year', secs, down, up, counter
    info['lastyear']['downtime'] = downtime
    info['lastyear']['up'] = up
    info['lastyear']['down'] = down
    info['lastyear']['times'] = counter


    alarm_query_down = Alarm.objects.filter(
        control_point=cpoint,
        up__isnull=True).order_by('down').reverse()
    alarm_query_up = Alarm.objects.filter(
        control_point=cpoint,
        up__isnull=False,
        down__gt=timezone.now() - datetime.timedelta(
            days=7)).order_by('down').reverse()
    alarm = False
    if len(Alarm.objects.filter(shown=False)) > 0:
        alarm = True
        for al in Alarm.objects.filter(shown=False):
            al.shown = True
            al.save()

    return render(request, 'showcp.html', {
        'cpoint': cpoint,
        'info': info,
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

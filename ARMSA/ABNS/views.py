# Create your views here.
# coding: utf-8
from django.shortcuts import render, HttpResponse, redirect
from .models import *
from ABNS.include.ping import do_one
from ABNS.include.snmp import *
from django.contrib.auth import logout
import logging
from django.contrib.auth.decorators import login_required

log = logging.getLogger(__name__)


def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return redirect('/login')


@login_required
def ABNS(request):
    street = {}
    streets_query = Street.objects.all().order_by('long_name')
    for s in streets_query:
        street[s.short_name] = s.pk
    clients_query = Client.objects.all()
    return render(request, "ABNS.html", {'streets_query': streets_query,
                                         'streets_pk': street,
                                         'clients_query': clients_query})


@login_required
def search(request):
    if request.method == 'GET':
        postdata = request.GET
        dogovor = postdata['dogovor']
        ip = postdata['ip']
        mac = postdata['mac']

        streets = Street.objects.all().order_by('long_name')
        entries = Client.objects.all()
        if (dogovor != ""):
            entries = entries.filter(dogovor__contains=dogovor)
        if (ip != ""):
            entries = entries.filter(ip__contains=ip)
        if (mac != ""):
            entries = entries.filter(mac__contains=mac.replace('%3A', ':'))
        entries = entries.extra(select={'flatint': 'CAST(REPLACE(REPLACE(REPLACE(REPLACE(flat,"b",""),"B",""),"a",""),"A","") AS UNSIGNED)'}).order_by('street__id', 'house', 'flatint')
        query = []
        status_ports = {}
        status_links = {}
        for e in entries:
            query.append(e.switch.sw_ip+':'+str(e.sw_port))
        status_ports, status_links = get_query_port_link(query)

    return render(request, "results.html", {'entries': entries,
                                            'streets': streets,
                                            'ports': status_ports,
                                            'links': status_links})


@login_required
def clients(request, st='2', ho='1'):
    entries = Client.objects.filter(street=int(st)).filter(house=ho).extra(
        select={'flatint': 'CAST(REPLACE(REPLACE(REPLACE(REPLACE(flat,"b",""),\
            "B",""),"a",""),"A","") AS UNSIGNED)'}).order_by('flatint')
    streets = Street.objects.all()
    entrance = entries[:1].get().entrance
    query = []
    status_ports = {}
    status_links = {}

    if request.method == 'POST':
        postdata = request.POST
        change_client = Client.objects.get(id=postdata['id'])
        change_client.ip = postdata['ip']
        if change_client.ip[3] in '1234':
            change_client.entrance = int(change_client.ip[3])
        else:
            change_client.entrance = 51
        change_client.main_ip = postdata['main_ip']
        change_client.dogovor = postdata['dogovor']
        change_client.street = Street.objects.get(pk=postdata['street'])
        change_client.house = postdata['house']
        change_client.flat = postdata['flat']
        change_client.save(
            update_fields=['ip', 'main_ip', 'dogovor', 'street',
                           'house', 'flat', 'entrance'])
        return HttpResponse(status=200)

    for client in entries:
        if client.switch.sw_ip != '0.0.0.0':
            query.append(client.switch.sw_ip+':'+str(client.sw_port))
    status_ports, status_links = get_query_port_link(query)
    c = {'entries': entries,
         'streets': streets,
         'entrance': entrance,
         'st_id': st,
         'ho_id': ho,
         'ports': status_ports,
         'links': status_links}

    return render(request, "clients.html", c)


@login_required
def ports(request, st='2', ho='1'):
    entries = Client.objects.filter(street=int(st)).filter(house=ho).extra(
        select={'flatint': 'CAST(REPLACE(REPLACE(REPLACE(REPLACE(flat,"b",""),\
            "B",""),"a",""),"A","") AS UNSIGNED)'}).order_by('flatint')
    for i in entries:
        print i.street.short_name, i.house, i.flat, i.id
    street = Street.objects.get(pk=int(st))
    if request.method == 'POST':
        postdata = request.POST
        change_client = Client.objects.get(pk=postdata['id'])
        change_client.ip = postdata['ip']
        if change_client.ip[3] in '1234':
            change_client.entrance = int(change_client.ip[3])
        else:
            change_client.entrance = 51
        change_client.main_ip = postdata['main_ip']
        change_client.house = postdata['house']
        change_client.flat = postdata['flat']
        change_client.mac = postdata['mac'].replace('%3A', ':')
        change_client.switch = Switch.objects.get(sw_ip=postdata['sw_ip'])
        change_client.sw_port = int(postdata['sw_port'])
        print change_client.mac, change_client.switch, change_client.sw_port
        change_client.save(
            update_fields=['ip', 'main_ip', 'house', 'flat',  'entrance',
                           'mac', 'switch', 'sw_port'])
        return HttpResponse(status=200)
    return render(request, "ports.html", {'entries': entries,
                                          'street': street,
                                          'st_id': st,
                                          'ho_id': ho})


@login_required
def delete_id(request):
    if request.method == 'GET':
        i = int(request.GET['id'])
        print i
        e = Client.objects.get(id=i)
        log.info(request.user.username + " deleted client " + str(e))
        e.delete()
    return HttpResponse(status=200)


@login_required
def delete_mac(request):
    if request.method == 'GET':
        i = int(request.GET['id'])
        print i
        e = Macs.objects.get(id=i)
        e.delete()
    return HttpResponse(status=200)


@login_required
def activate_id(request):
    if request.method == 'GET':
        i = int(request.GET['id'])
        a = request.GET['act']
        e = Client.objects.get(id=i)
        if a == "True":
            e.active_state = True
        else:
            e.active_state = False
        log.info(request.user.username + " activated client " + str(e))
        e.save()
    return HttpResponse(status=200)


@login_required
def lock_id(request):
    if request.method == 'GET':
        i = int(request.GET['id'])
        a = request.GET['act']
        e = Client.objects.get(id=i)
        if a == "True":
            e.lock_state = True
        else:
            e.lock_state = False
        log.info(request.user.username + " locked client " + str(e))
        e.save()
    return HttpResponse(status=200)


@login_required
def portaction(request):
    if request.method == 'GET':
        sw = request.GET['sw']
        port = int(request.GET['port'])
        act = request.GET['act']

        if act == "open":
            openport(sw, port)
            log.info(request.user.username + " opened port " + sw + ':' + port)
        else:
            log.info(request.user.username + " closed port " + sw + ':' + port)
            closeport(sw, port)
    return HttpResponse(status=200)


@login_required
def trustaction(request):
    if request.method == 'GET':
        sw = request.GET['sw']
        port = int(request.GET['port'])
        act = request.GET['act']

        e = Macs.objects.filter(switch__sw_ip=sw, sw_port=port)

        if len(e) > 0:
            if act == "check":
                e[0].trusted = True
                log.info(request.user.username + " set trusted " + sw + ':' + port)
            else:
                e[0].trusted = False
                log.info(request.user.username + " set untrusted " + sw + ':' + port)
            e[0].save()
        else:
            if act == "check":
                a = True
            else:
                a = False
            s = Switch.objects.get(pk=int(sw))
            n = Macs(switch=sw, sw_port=port, mac='', trusted=a)
            n.save()
    return HttpResponse(status=200)


@login_required
def switches(request, st='2', ho='1'):
    sw_query = Switch.objects.filter(street=int(st), house=ho)
    ports = {}
    sw_pings = {}
    status_ports = {}
    status_links = {}
    status_trust = {}
    port_address = {}
    port_type = {}
    port_memo = {}
    port_types = SwInfo.objects.all()

    if request.method == 'POST':
        postdata = request.POST
        print postdata
        change_client = PortInfo.objects.filter(sw_sn=postdata['sn'],
                                                sw_port=postdata['port'])
        if len(change_client) != 0:
            change_client[0].sw_info = SwInfo.objects.get(pk=int(postdata['type']))
            change_client[0].sw_memo = postdata['memo']
            change_client[0].save(update_fields=['sw_info', 'sw_memo'])
        else:
            new = PortInfo(sw_sn=postdata['sn'],
                           sw_port=postdata['port'],
                           sw_info=SwInfo.objects.get(pk=int(postdata['type'])),
                           sw_memo=postdata['memo'])
            new.save()
        return HttpResponse(status=200)
    else:
        for s in sw_query:
            # print(s.sw_ip)
            sw_pings[s.sw_ip] = do_one(s.sw_ip)
            portnumber = s.sw_type.ports
            ports[s.sw_ip] = portnumber
            p, l = get_ports_links(s.sw_ip, portnumber)
            status_ports = dict(status_ports.items() + p.items())
            status_links = dict(status_links.items() + l.items())

            for i in range(portnumber):
                swp = (s.sw_ip + ':' + str(i + 1))
                macs_q = Macs.objects.filter(switch=s, sw_port=i + 1)
                if len(macs_q) > 0:
                    status_trust[swp] = macs_q[0].trusted
                else:
                    status_trust[swp] = False
                cl_q = Client.objects.filter(switch=s, sw_port=i + 1)
                if len(cl_q) > 0:
                    port_address[swp] = cl_q[0].street.short_name + '-'
                    port_address[swp] = port_address[swp] + cl_q[0].house + '-'
                    port_address[swp] = port_address[swp] + cl_q[0].flat
                else:
                    port_address[swp] = '---'
                info_q = PortInfo.objects.filter(sw_sn=s.sw_sn, sw_port=i + 1)
                if len(info_q) > 0:
                    port_type[swp] = info_q[0].sw_info.id
                    port_memo[swp] = info_q[0].sw_memo
                else:
                    port_type[swp] = 2
                    port_memo[swp] = ''

    return render(request, "switches.html", {'sw_query': sw_query,
                                             'ports': ports,
                                             'pings': sw_pings,
                                             'status_ports': status_ports,
                                             'status_links': status_links,
                                             'status_trust': status_trust,
                                             'port_address': port_address,
                                             'port_types': port_types,
                                             'port_type': port_type,
                                             'port_memo': port_memo,
                                             'st_id': st,
                                             'ho_id': ho})


@login_required
def mac(request, st='2', ho='1'):
    macs_dict = {}
    sw_pings = {}
    status_ports = {}
    status_links = {}
    status_trust = {}
    port_address = {}

    if request.method == 'POST':
        postdata = request.POST
        macid = postdata['id'] 
        newmac = postdata['mac'].replace('%3A', ':')
        edit = Macs.objects.get(pk=macid)
        edit.mac = newmac
        edit.save(update_fields=['mac'])
        return HttpResponse(status=200)
    else:

        sw_query = Switch.objects.filter(street=int(st), house=ho)
        for sw in sw_query:
            macs_q = Macs.objects.filter(switch=sw).order_by('sw_port')
            macs_dict[sw.sw_ip] = macs_q
            sw_pings[sw.sw_ip] = do_one(sw.sw_ip)
            portnumber = sw.sw_type.ports
            p, l = get_ports_links(sw.sw_ip, portnumber)
            status_ports = dict(status_ports.items() + p.items())
            status_links = dict(status_links.items() + l.items())

            for i in range(portnumber):
                swp = (sw.sw_ip + ':' + str(i + 1))
                macsq = macs_q.filter(sw_port=i + 1)
                if len(macsq) > 0:
                    status_trust[swp] = macsq[0].trusted
                else:
                    status_trust[swp] = False

                cl_q = Client.objects.filter(switch=sw, sw_port=i + 1)
                if len(cl_q) > 0:
                    port_address[swp] = cl_q[0].street.short_name + '-'
                    port_address[swp] = port_address[swp] + cl_q[0].house
                    port_address[swp] = port_address[swp] + '-' + cl_q[0].flat
                else:
                    port_address[swp] = '---'
        print sw_query

    return render(request, "macs.html", {'sw_query': sw_query,
                                         'macs_dict': macs_dict,
                                         'status_ports': status_ports,
                                         'status_links': status_links,
                                         'port_address': port_address,
                                         'status_trust': status_trust,
                                         'st_id': st,
                                         'ho_id': ho})

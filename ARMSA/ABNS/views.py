# Create your views here.
# coding: utf-8
from django.shortcuts import render, HttpResponse
from .models import client, street, switch, sw_info, sw_type, ports_info, macs
from ABNS.include.ping import do_one
from ABNS.include.snmp import get_ports_links, get_one_ports_links


def ABNS(request, st="Ba", ho="1"):
    print(do_one("127.0.0.1"))
    streets_query = street.objects.all().order_by('long_name')
    clients_query = client.objects.all()
    address_query = client.objects.filter(street=st).filter(house=ho)
    #form = UserRowForm()
    return render(request, "ABNS.html", {'streets_query': streets_query, 'clients_query': clients_query, 'address_query': address_query})


def search(request):
    if request.method == 'GET':
        postdata = request.GET
        dogovor = postdata['dogovor']
        ip = postdata['ip']
        mac = postdata['mac']

        streets = street.objects.all().order_by('long_name')
        entries = client.objects.all()
        if (dogovor != ""):
            entries = entries.filter(dogovor__contains=dogovor)
        if (ip != ""):
            entries = entries.filter(ip__contains=ip)
        if (mac != ""):
            entries = entries.filter(mac__contains=mac)

        sw_pings = {}
        status_ports = {}
        status_links = {}
        for e in entries:
            if e.sw_ip not in sw_pings:
                print(e.sw_ip)
                sw_pings[e.sw_ip] = do_one(e.sw_ip)
                p, l = get_one_ports_links(e.sw_ip,e.sw_port)
                status_ports = dict(status_ports.items() + p.items())
                status_links = dict(status_links.items() + l.items())

    return render(request, "results.html", {'entries': entries, 'streets': streets, 'pings': sw_pings, 'ports': status_ports, 'links': status_links})


def clients(request, st="Ba", ho="1"):
    entries = client.objects.filter(street=st, house=ho).extra(
        select={'flatint': 'CAST(REPLACE(REPLACE(REPLACE(REPLACE(flat,"b",""),"B",""),"a",""),"A","") AS UNSIGNED)'}).order_by('flatint')
    streets = street.objects.all()
    entrance = entries[:1].get()
    sw_pings = {}
    status_ports = {}
    status_links = {}
    for e in entries:
        if (e.sw_ip not in sw_pings) and (sw_pings != "0.0.0.0"):
            sw_pings[e.sw_ip] = do_one(e.sw_ip)
            sw = switch.objects.filter(sw_ip=e.sw_ip)
            if len(sw) > 0:
                portnumber = sw_type.objects.filter(sw_type=sw.get().sw_type)
                p, l = get_ports_links(e.sw_ip,portnumber.get().ports)
                status_ports = dict(status_ports.items() + p.items())
                status_links = dict(status_links.items() + l.items())

    if request.method == 'POST':
        postdata = request.POST
        change_client = client.objects.get(id=postdata['id'])
        change_client.ip = postdata['ip']
        if change_client.ip[3] in '1234':
            change_client.entrance = int(change_client.ip[3])
        else:
            change_client.entrance = 51
        change_client.main_ip = postdata['main_ip']
        change_client.dogovor = postdata['dogovor']
        change_client.street = postdata['street']
        change_client.house = postdata['house']
        change_client.flat = postdata['flat']
        change_client.save(
            update_fields=['ip', 'main_ip', 'dogovor', 'street', 'house', 'flat', 'entrance'])
    return render(request, "clients.html", {'entries': entries, 'streets': streets, 'entrance': entrance.entrance, 'st_id': st, 'ho_id': ho, 'pings': sw_pings, 'ports': status_ports, 'links': status_links})


def ports(request, st="Ba", ho="1"):
    entries = client.objects.filter(street=st, house=ho).extra(
        select={'flatint': 'CAST(REPLACE(REPLACE(REPLACE(REPLACE(flat,"b",""),"B",""),"a",""),"A","") AS UNSIGNED)'}).order_by('flatint')
    entrance = entries[:1].get()
    st = street.objects.get(short_name=st)
    if request.method == 'POST':
        postdata = request.POST
        change_client = client.objects.get(id=postdata['id'])
        change_client.ip = postdata['ip']
        if change_client.ip[3] in '1234':
            change_client.entrance = int(change_client.ip[3])
        else:
            change_client.entrance = 51
        change_client.main_ip = postdata['main_ip']
        change_client.house = postdata['house']
        change_client.flat = postdata['flat']
        change_client.mac = postdata['mac'].replace('%3A', ':')
        change_client.sw_ip = postdata['sw_ip']
        change_client.sw_port = postdata['sw_port']
        change_client.save(
            update_fields=['ip', 'main_ip', 'house', 'flat', 'entrance', 'mac', 'sw_ip', 'sw_port'])
    return render(request, "ports.html", {'entries': entries, 'street': st, 'st_id': entrance.street, 'ho_id': entrance.house})


def delete_id(request):
    if request.method == 'GET':
        i = int(request.GET['id'])
        print i
        e = client.objects.get(id=i)
        e.delete()
    return HttpResponse(status=200)


def activate_id(request):
    if request.method == 'GET':
        i = int(request.GET['id'])
        a = request.GET['act']
        e = client.objects.get(id=i)
        if a == "True":
            e.active_state = True
        else:
            e.active_state = False
        e.save()
    return HttpResponse(status=200)


def lock_id(request):
    if request.method == 'GET':
        i = int(request.GET['id'])
        a = request.GET['act']
        e = client.objects.get(id=i)
        if a == "True":
            e.lock_state = True
        else:
            e.lock_state = False
        e.save()
    return HttpResponse(status=200)


def switches(request, st='Ba', ho='1'):
    sw_query = switch.objects.filter(street=st, house=ho)
    for s in sw_query:
        print(s.sw_ip)
        port_count = sw_type.objects.filter(sw_type=s.sw_type)[:1].get().ports
        print s.sw_sn
        sw = ports_info.objects.filter(sw_sn=s.sw_sn)
        print ("length of sw_q",len(sw))
        for p in range(port_count):
            macs_q = macs.objects.filter(sw_ip=s.sw_ip, sw_port=p+1)
            if len(macs_q)>0:
                trust = macs_q[0].trusted
            else: 
                trust = False
            cl_q = client.objects.filter(sw_ip=s.sw_ip, sw_port=p+1)
            if len(cl_q) > 0:
                cl = cl_q[0]
                address = cl.street+'-'+cl.house+'-'+cl.flat
            else:
                address = '---'
            
            if len(sw)==0:
                status = "Рабочий"
                memo = ''
            else:
                st_q = sw.filter(sw_port=p)
                if len(st_q):
                    status = st_q[0].sw_info
                    memo = st_q[0].sw_memo
                else:
                    status = "Рабочий"
                    memo = ''


            print(p, trust, address, status, memo)


    return HttpResponse(status=200)

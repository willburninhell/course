# Create your views here.
from django.shortcuts import render,HttpResponse
from .models import client, street


def ABNS(request, st="Ba", ho="1"):
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
#form = UserRowForm()

    return render(request, "results.html", {'entries': entries, 'streets': streets})


def clients(request, st="Ba", ho="1"):
    print "here"
    entries = client.objects.filter(street=st, house=ho).extra(
        select={'flatint': 'CAST(REPLACE(REPLACE(REPLACE(REPLACE(flat,"b",""),"B",""),"a",""),"A","") AS UNSIGNED)'}).order_by('flatint')
    print "here2"
    streets = street.objects.all()
    print "here3"
    entrance = entries[:1].get()
    print "here4"

    if request.method == 'POST':
        print "here5"
        postdata = request.POST

        if "mac" in postdata:
            print "search"
        else:
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
    return render(request, "clients.html", {'entries': entries, 'streets': streets, 'entrance':entrance.entrance, 'st_id':st, 'ho_id':ho})


def ports(request, st="Ba", ho="1"):
    entries = client.objects.filter(street=st, house=ho).extra(
        select={'flatint': 'CAST(REPLACE(REPLACE(REPLACE(REPLACE(flat,"b",""),"B",""),"a",""),"A","") AS UNSIGNED)'}).order_by('flatint')
    st = street.objects.get(short_name=st)
    return render(request, "ports.html", {'entries': entries, 'street': st, 'st_id':st, 'ho_id':ho})


def delete_id(request):
    print "delete"
    if request.method == 'GET':
        i = int(request.GET['id'])
        print i
        e = client.objects.get(id=i)
        e.delete()
    return HttpResponse(status=200)

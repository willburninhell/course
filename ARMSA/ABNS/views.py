# Create your views here.
from django.shortcuts import render
from .models import client, street


def streets_view(request,st="Ba",ho="1"):
    streets_query = street.objects.all().order_by('long_name')
    clients_query = client.objects.all()
    address_query = client.objects.filter(street=st).filter(house=ho)
    #form = UserRowForm()

    if request.method == 'POST':
        postdata = request.POST
        # print postdata['id']
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

    return render(request, "streettree.html", {'streets_query': streets_query, 'clients_query': clients_query, 'address_query': address_query})


def abns(request):
    streets_query = street.objects.all().order_by('long_name')
    clients_query = client.objects.all()
    #form = UserRowForm()
    return render(request, "abns.html", {'streets_query': streets_query, 'clients_query': clients_query})


def clients(request,st="Ba",ho="1"):
    entries = client.objects.filter(street=st, house=ho).extra(
        select={'flatint': 'CAST(REPLACE(REPLACE(REPLACE(REPLACE(flat,"b",""),"B",""),"a",""),"A","") AS UNSIGNED)'}).order_by('flatint')
    streets = street.objects.all()
    #form = UserRowForm()

    if request.method == 'POST':
        postdata = request.POST
        # print postdata['id']
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

    return render(request, "clients.html", {'entries': entries, 'streets': streets})

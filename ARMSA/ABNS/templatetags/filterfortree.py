from django import template
from pysnmp.entity.rfc3413.oneliner import cmdgen

register = template.Library()


@register.filter
def filter_house(query, arg):
    qq = query.filter(street=arg)
    qq = qq.values('house').distinct()
    qq = qq.extra(select={'houseint': "CAST(house AS SIGNED INTEGER)"})
    qq = qq.extra(order_by=['houseint'])
    # print qq
    return qq


@register.filter
def check_sw(ip, sw_ping):
    if (sw_ping[ip] > 0):
        return True
    else:
        return False

@register.filter
def check_port(sw_ip_port, ports_data):
    print("check port",sw_ip_port,ports_data[sw_ip_port])
    if ports_data[sw_ip_port] == '1':
        return True
    else:
        return False

@register.filter
def check_link(sw_ip_port, ports_data):
    if ports_data[sw_ip_port] == '1':
        return True
    else:
        return False
from django import template

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

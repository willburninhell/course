from django import template

register = template.Library()


@register.filter
def filter_house(query, arg):
    print arg
    qq = query.filter(street=arg)
    qq = qq.values('house').distinct()
    qq = qq.extra(select={'houseint': "CAST(house AS SIGNED INTEGER)"})
    qq = qq.extra(order_by = ['houseint'])
    #print qq
    return qq

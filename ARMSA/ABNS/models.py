from django.db import models

# Create your models here.


class client(models.Model):
    ip = models.CharField(max_length=15, default='0.0.0.0')
    main_ip = models.CharField(max_length=15, default='0.0.0.0')
    mac = models.CharField(max_length=17, default='00:00:00:00:00:00')
    dogovor = models.CharField(max_length=32, default='000000')
    street = models.CharField(max_length=4)
    house = models.CharField(max_length=4,default='0')
    flat = models.CharField(max_length=4)
    entrance = models.IntegerField(default=0)
    sw_ip = models.CharField(max_length=15, default="0.0.0.0")
    sw_port = models.IntegerField(default=0)
    lock_state = models.BooleanField(default=False)
    active_state = models.BooleanField(default=False)
    inet_limit = models.IntegerField(default=0)
    local_limit = models.IntegerField(default=0)
    vpn_type = models.IntegerField(default=0)
    block_local = models.BooleanField(default=False)
    block_inet = models.BooleanField(default=False)
    email = models.EmailField(default='')

    def __unicode__(self):
        return self.street + "-" + self.house + "-" + self.flat


class street(models.Model):
    short_name = models.CharField(max_length=4)
    long_name = models.CharField(max_length=256)

    def __unicode__(self):
        return self.long_name

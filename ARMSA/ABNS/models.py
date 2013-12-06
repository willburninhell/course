from django.db import models

# Create your models here.


class client(models.Model):
    ip = models.CharField(max_length=15, default='0.0.0.0')
    main_ip = models.CharField(max_length=15, default='0.0.0.0')
    mac = models.CharField(max_length=17, default='00:00:00:00:00:00')
    dogovor = models.CharField(max_length=32, default='000000')
    street = models.CharField(max_length=4)
    house = models.CharField(max_length=4, default='0')
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


class switches(models.Model):
    sw_ip = models.CharField(max_length=15, default="10.254.0.0")
    sw_mac = models.CharField(max_length=17, default="00:00:00:00:00:00")
    sw_sn = models.CharField(max_length=15, default="000000000000000")
    sw_type = models.CharField(max_length=15, default="HPProCurve-2626")
    sw_ro = models.CharField(max_length=15, default="WGS_RO")
    sw_wr = models.CharField(max_length=15, default="SW_wRITE")
    street = models.CharField(max_length=4)
    house = models.CharField(max_length=4, default="0")
    entrance = models.IntegerField(default=0)

    def __unicode__(self):
        return self.sw_ip


class sw_info(models.Model):
    sw_info = models.CharField(max_length=32)

    def __unicode__(self):
        return self.sw_info


class sw_type(models.Model):
    sw_type = models.CharField(max_length=15, default="HPProCurve-2626")
    ports = models.IntegerField(default=0)

    def __unicode__(self):
        return self.sw_type


class ports_info(models.Model):
    sw_sn = models.CharField(max_length=15, default="000000000000000")
    sw_port = models.IntegerField(default=0)
    sw_info = models.CharField(max_length=32)
    sw_memo = models.CharField(max_length=255)

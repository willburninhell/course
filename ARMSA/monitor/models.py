from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=32, default='NoName')
    description = models.CharField(max_length=255, default='')

    def __unicode__(self):
        return self.name


class ControlPoint(models.Model):
    name = models.CharField(max_length=32, default='NoName')
    ip = models.CharField(max_length=15, default='0.0.0.0')
    description = models.CharField(max_length=255, default='', blank=True)
    group = models.ForeignKey(Group)


class Alarm(models.Model):
    control_point = models.ForeignKey(ControlPoint)
    down = models.DateTimeField(auto_now_add=True)
    up = models.DateTimeField(null=True)
    comment = models.TextField(default="")

    def __unicode__(self):
        return self.name

from django.db import models
from django.contrib.auth.models import User
import datetime


class WorkingDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today, unique=True)
    check_in = models.TimeField(blank=True, null=True, auto_now=False, auto_now_add=False)
    check_out = models.TimeField(blank=True, null=True, auto_now=False, auto_now_add=False)
    vacation = models.BooleanField(default=False)

    # calculate duration between check in and out
    def duration(self):
        if not isinstance(self.check_out, type(None)) and not isinstance(self.check_in, type(None)):
            check_out_time = datetime.timedelta(hours=self.check_out.hour, minutes=self.check_out.minute, seconds=self.check_out.second)
            check_in_time = datetime.timedelta(hours=self.check_in.hour, minutes=self.check_in.minute, seconds=self.check_in.second)
            return check_out_time-check_in_time
        else:
            return None

    class Meta:
        ordering = ["date"]

    def __str__(self):
        return 'ID:'+str(self.pk)+', user: '+self.user.username+', Date:'+str(self.date)


class LeavingTime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    start = models.TimeField(default=datetime.time(00, 00), auto_now=False, auto_now_add=False)
    end = models.TimeField(default=datetime.time(00, 00), auto_now=False, auto_now_add=False)

    def duration(self):
        end_time = datetime.timedelta(hours=self.end.hour, minutes=self.end.minute, seconds=self.end.second)
        start_time = datetime.timedelta(hours=self.start.hour, minutes=self.start.minute, seconds=self.start.second)
        return end_time-start_time

    def __str__(self):
        return str(self.pk)+" - "+str(self.user.username)+" - "+str(self.date)

    class Meta:
        ordering = ["date"]
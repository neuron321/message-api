from django.db import models

# Create your models here.


class Account(models.Model):
    auth_id = models.CharField(max_length=40, blank=True, null=True)
    username = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'account'


class PhoneNumber(models.Model):
    number = models.CharField(max_length=40, blank=True, null=True)
    account = models.ForeignKey(
        Account, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'phone_number'


class SMS(models.Model):
    sender = models.ForeignKey(
        PhoneNumber, on_delete=models.DO_NOTHING, related_name='sms_sender')
    to = models.ForeignKey(
        PhoneNumber, on_delete=models.DO_NOTHING, related_name='sms_receiver')
    text = models.CharField(max_length=120, blank=False, null=False)

    class Meta:
        db_table = 'sms'

from django.urls import path
from . import views

urlpatterns = [
    path('inbound/sms/',
         views.SMSList, name="sms-inbound"),
    path('outbound/sms/',
         views.OutboundSMSList, name="sms-outbound"),
]

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^twilio/sms/$', views.receive_twilio_sms),
]

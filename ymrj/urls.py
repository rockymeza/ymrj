from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='welcome.html')),
    url(r'^ingress/', include('ingress.urls')),
    url(r'^admin/', admin.site.urls),
]

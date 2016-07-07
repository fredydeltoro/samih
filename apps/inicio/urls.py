from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import InicioView, CausesView, PrincipalView

urlpatterns = [
    url(r'^$', InicioView.as_view(), name='inicio'),
    url(r'^causes/(?P<pk>\d+)/$', CausesView.as_view(), name="causes"),
    url(r'^principal/$', login_required(PrincipalView.as_view(template_name='principal.html'))),
]
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import ProdUrg

urlpatterns = [
	url(r'^urgencias/productividad/$', login_required(ProdUrg.as_view(template_name='productividad_urg.html')), name="farmacia"),
]
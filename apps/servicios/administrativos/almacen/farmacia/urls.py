from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from .views import FarmaciaView, CrearSolFarmVentaView, SolFarmVentaView, PdfSolFarmVentaView, CrearSolFarmSegPopView, SolFarmSegPopView, PdfSolFarmSegPopView, CrearSolFarmMedControladoView, SolFarmMedControladoView, PdfSolFarmMedControlaView

urlpatterns = [
	url(r'^farmacia/$', login_required(FarmaciaView.as_view(template_name='farmacia.html')), name="farmacia"),

	#Solicitud de Farmacia: Venta al publico
	url(r'^farmacia/solfarmventa/(?P<pk>\d+)/$', login_required(SolFarmVentaView.as_view(template_name='solfarmventa.html')),name="solfarmventa"),
	url(r'^farmacia/crearsolfarmventa/$', login_required(CrearSolFarmVentaView.as_view(template_name='crearsolfarmventa.html')), name="crearsolfarmventa"),
	url(r'^farmacia/solfarmventapdf/(?P<solfarm_id>\d+)/$', login_required(PdfSolFarmVentaView), name="solfarmventapdf"),

	#Solicitud de Farmacia: Seguro Popular
	url(r'^farmacia/solfarmsegpop/(?P<pk>\d+)/$', login_required(SolFarmSegPopView.as_view(template_name='solfarmsegpop.html')),name="solfarmsegpop"),
	url(r'^farmacia/crearsolfarmsegpop/$', login_required(CrearSolFarmSegPopView.as_view(template_name='crearsolfarmsegpop.html')), name="crearsolfarmsegpop"),
	url(r'^farmacia/solfarmsegpoppdf/(?P<solfarm_id>\d+)/$', login_required(PdfSolFarmSegPopView), name="solfarmsegpoppdf"),

	#Solicitud de Farmacia: Medicamento Controlado
	url(r'^farmacia/solfarmmedcontrolado/(?P<pk>\d+)/$', login_required(SolFarmMedControladoView.as_view(template_name='solfarmmedcontrolado.html')),name="solfarmmedcontrolado"),
	url(r'^farmacia/crearsolfarmmedcontrolado/$', login_required(CrearSolFarmMedControladoView.as_view(template_name='crearsolfarmmedcontrolado.html')), name="crearsolfarmmedcontrolado"),
	url(r'^farmacia/solfarmmedcontroladopdf/(?P<solfarm_id>\d+)/$', login_required(PdfSolFarmMedControlaView), name="solfarmmedcontroladopdf"),
]
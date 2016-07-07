#encoding=utf-8
import json

from django.http import HttpResponse
from django.db.models import Count
from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView, DetailView

from datetime import datetime
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.colors import HexColor, black
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter, cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle, SimpleDocTemplate

from .forms import SolicitudFarmaciaForm, ItemSolFarmFormSet, ItemSolFarmMedControladoFormSet
from .models import SolicitudFarmacia, ItemSolFarm

FORMATO_DIA= '%m/%d/%Y'
logoSAMIH = ImageReader('static/img/SIHos_512.png')
logoHGSJR = ImageReader('static/img/logo_hgsjr.png')
logoSSA = ImageReader('static/img/logo_ssa.png')

class FormsetMixin(object):
	object = None

	def get(self, request, *args, **kwargs):
		if getattr(self, 'is_update_view', False):
			self.object = self.get_object()
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		formset_class = self.get_formset_class()
		formset = self.get_formset(formset_class)
		return self.render_to_response(self.get_context_data(form=form, formset=formset))

	def post(self, request, *args, **kwargs):
		if getattr(self, 'is_update_view', False):
			self.object = self.get_object()
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		formset_class = self.get_formset_class()
		formset = self.get_formset(formset_class)
		if form.is_valid() and formset.is_valid():
			return self.form_valid(form, formset)
		else:
			return self.form_invalid(form, formset)

	def get_formset_class(self):
		return self.formset_class

	def get_formset(self, formset_class):
		return formset_class(**self.get_formset_kwargs())

	def get_formset_kwargs(self):
		kwargs = {
			'instance': self.object
		}
		if self.request.method in ('POST', 'PUT'):
			kwargs.update({
				'data': self.request.POST,
				'files': self.request.FILES,
			})
		return kwargs

	def form_valid(self, form, formset):
		self.object = form.save()
		formset.instance = self.object #Con esto agrego al modelo el usuario logueado
		formset.save()
		return redirect(self.object.get_absolute_url())

	def form_invalid(self, form, formset):
		return self.render_to_response(self.get_context_data(form=form, formset=formset))


class FarmaciaView(TemplateView):
	template_name = 'farmacia.html'

	def get_context_data(self, **kwargs):
	    context = super(FarmaciaView, self).get_context_data(**kwargs)
	    context['solicitudes'] = SolicitudFarmacia.objects.all()
	    return context


#### Solicitud de Farmacia: Venta al público ###################################
class CrearSolFarmVentaView(FormsetMixin, CreateView):
	template_name = 'crearsolfarmventa.html'
	model = SolicitudFarmacia
	form_class = SolicitudFarmaciaForm
	formset_class = ItemSolFarmFormSet

	def get_context_data(self, **kwargs):
	    context = super(CrearSolFarmVentaView, self).get_context_data(**kwargs)
	    context['Hoy'] = datetime.now()
	    return context

	def form_valid(self, form, formset):
		form.instance.usuario = self.request.user
		form.instance.tiposol = 'venta'
		return super(CrearSolFarmVentaView, self).form_valid(form, formset)


class SolFarmVentaView(DetailView):
	template_name = 'solfarmventa.html'
	model = SolicitudFarmacia


def PdfSolFarmVentaView(request, solfarm_id):
	response = HttpResponse(content_type = 'application/pdf')
	response['Content-Disposition'] = 'filename = "solfarmventa.pdf"'

	buffer = BytesIO()

	p = canvas.Canvas(buffer, pagesize = letter)

	#Cabecera
	p.drawImage(logoHGSJR, 15,750, 90, 40, mask='auto')
	p.drawImage(logoSSA, 190,750, 90, 40, mask='auto')
	p.setFont('Helvetica', 8)
	p.drawString(65, 750, "HOSPITAL GENERAL DE SAN JUAN DEL RÍO")
	p.setFont('Helvetica-Bold', 8)
	p.drawString(87, 741, "DEPARTAMENTO DE FARMACIA")
	p.setFont('Helvetica', 8)
	solfarm = [(sf.id,sf.fecha_creacion,sf.paciente,sf.receta,sf.poliza_segpop) for sf in SolicitudFarmacia.objects.filter(pk = solfarm_id)]
	for sfv in solfarm:
		p.setFont('Helvetica', 8)
		p.drawString(15, 730, "FOLIO:")
		p.drawCentredString(72, 730, str(sfv[0]))
		p.line(42,728,100,728)

		p.drawString(207, 730, "FECHA:")
		fecha = datetime.strftime(sfv[1], FORMATO_DIA) #Darle formato a la fecha
		p.drawString(238, 730, str(fecha))
		p.line(237,728,280,728)
		
		#Datos paciente
		p.drawString(15, 718, "PACIENTE:")
		p.drawCentredString(170, 718, str(sfv[2]))
		p.line(59,716,280,716)

		p.drawString(15, 706, "RECETA:")
		p.drawCentredString(70, 706, str(sfv[3]))
		p.line(51,704,90,704)

	#Medicamentos
	data = []

	medicamentos = [(m.medicamento.clave_farmacia,m.cantidad_surtida,m.medicamento.nombre,m.medicamento.presentacion,m.medicamento.precio) for m in ItemSolFarm.objects.filter(solfarm_id=solfarm_id)]

	styles = getSampleStyleSheet()
	styleN = styles["BodyText"]
	styleN.alignment = TA_CENTER
	styleN.fontSize = 6

	for meds in medicamentos:
		precio_med = meds[1] * meds[4]
		this_meds = [meds[0],meds[1],Paragraph(meds[2], styleN),meds[3],Paragraph("$" + str(meds[4]), styleN),Paragraph("$" + str(precio_med), styleN)]
		data.append(this_meds)

	width, height = letter
								   # clave      cant       med        umed       fcad       lote
	table = Table(data, colWidths = [0.88 * cm, 0.83 * cm, 3.74 * cm, 1.02 * cm, 1.43 * cm, 1.43 * cm],
						 rowHeights = len(data) * [-0.939 * cm],)
	table.setStyle(TableStyle([
			('ALIGN', (0,0), (-1,-1), 'CENTER'), #Alineacion de las columnas
	        ('FONTSIZE', (0,0), (-1,-1), 7), #Tamaño de la fuente de la tabla
	        #('GRID', (0,1), (5,len(data)-1), 0.75, colors.black),
		]))
	table.wrapOn(p, width, height)
	table.drawOn(p, 15, 660)

	p.setFillColor(HexColor('#B6B6B6'))
	p.rect(15,688,265,12, fill=1, stroke=False)
	p.line(15,688,280,688)
	p.line(15,475,280,475)
	p.line(15,463,280,463)
	p.line(65,452,65,475)
	p.line(15,661,280,661)
	p.line(15,633,280,633)
	p.line(15,605,280,605)
	p.line(15,579,280,579)
	p.line(15,553,280,553)
	p.line(15,527,280,527)
	p.line(15,501,280,501)

	p.setFillColor(black)
	p.setFont("Helvetica-Bold", 6)
	p.drawString(17, 691, "CLAVE")
	p.drawString(43, 691, "CANT")
	p.drawString(95, 691, "MEDICAMENTO")
	p.drawString(174, 691, "U.MED")
	p.drawString(211, 691, "P.UNI")
	p.drawString(249, 691, "TOTAL")

	#Datos del medico
	p.drawString(27, 466, "MÉDICO")
	p.drawString(23, 455, "SERVICIO")
	medico = [(md.medico,md.medico.servicio) for md in SolicitudFarmacia.objects.filter(pk = solfarm_id)]
	for dr in medico:
		p.drawCentredString(170, 466, str(dr[0])) #Medico
		p.drawCentredString(170, 455, str(dr[1])) #Servicio

	p.line(40,475,40,700) #clave|cant
	p.line(63,475,63,700) #cant|med
	p.line(169,475,169,700) #med|umed
	p.line(198,475,198,700) #umed|fcad
	p.line(239,475,239,700) #fcad|lote
	p.setFillColor(black)
	p.rect(15,452,265,248, fill=False, stroke=1) #Caja de grilla medicamentos

	#Pie de página
	p.setFont('Helvetica', 8)
	usuario = [(us.usuario, us.fecha_creacion) for us in SolicitudFarmacia.objects.filter(pk = solfarm_id)]
	for entrego in usuario:
		p.drawCentredString(60,418, str(entrego[0])) #Usuario
	p.line(20,414,100,414)
	p.setFont('Helvetica', 6)
	p.drawCentredString(60,405, "E N T R E G A")
	p.drawImage(logoSAMIH, 258,416, 15, 15, mask='auto')
	p.setFont('Helvetica', 6)
	p.drawString(256, 411, "SAMIH")
	p.setFont('Helvetica', 3)
	p.drawString(256, 408, "by DVLC")

	p.showPage()
	p.save()
	pdf = buffer.getvalue()
	buffer.close()
	response.write(pdf)
	return response
############################################################################################

#### Solicitud de Farmacia: Seguro Popular #################################################
class CrearSolFarmSegPopView(FormsetMixin, CreateView):
	template_name = 'crearsolfarmsegpop.html'
	model = SolicitudFarmacia
	form_class = SolicitudFarmaciaForm
	formset_class = ItemSolFarmFormSet

	def get_context_data(self, **kwargs):
	    context = super(CrearSolFarmSegPopView, self).get_context_data(**kwargs)
	    context['Hoy'] = datetime.now()
	    return context

	def form_valid(self, form, formset):
		form.instance.usuario = self.request.user
		form.instance.tiposol = 'segpop'
		return super(CrearSolFarmSegPopView, self).form_valid(form, formset)


class SolFarmSegPopView(DetailView):
	template_name = 'solfarmsegpop.html'
	model = SolicitudFarmacia


def PdfSolFarmSegPopView(request, solfarm_id):
	response = HttpResponse(content_type = 'application/pdf')
	response['Content-Disposition'] = 'filename = "solfarmsegpop.pdf"'

	buffer = BytesIO()

	p = canvas.Canvas(buffer, pagesize = letter)

	#Cabecera
	p.drawImage(logoHGSJR, 15,750, 90, 40, mask='auto')
	p.drawImage(logoSSA, 190,750, 90, 40, mask='auto')
	p.setFont('Helvetica', 8)
	p.drawString(65, 750, "HOSPITAL GENERAL DE SAN JUAN DEL RÍO")
	p.setFont('Helvetica-Bold', 8)
	p.drawString(87, 741, "DEPARTAMENTO DE FARMACIA")
	p.setFont('Helvetica', 8)
	solfarm = [(sf.id,sf.fecha_creacion,sf.paciente,sf.receta,sf.poliza_segpop) for sf in SolicitudFarmacia.objects.filter(pk = solfarm_id)]
	for sfsp in solfarm:
		p.setFont('Helvetica', 8)
		p.drawString(15, 730, "FOLIO:")
		p.drawCentredString(72, 730, str(sfsp[0]))
		p.line(42,728,100,728)

		p.drawString(207, 730, "FECHA:")
		fecha = datetime.strftime(sfsp[1], FORMATO_DIA) #Darle formato a la fecha
		p.drawString(238, 730, str(fecha))
		p.line(237,728,280,728)
		
		#Datos paciente
		p.drawString(15, 718, "PACIENTE:")
		p.drawCentredString(170, 718, str(sfsp[2]))
		p.line(59,716,280,716)

		p.drawString(15, 706, "RECETA:")
		p.drawCentredString(70, 706, str(sfsp[3]))
		p.line(51,704,90,704)

		p.drawString(110,706, "PÓLIZA DE SEGURO POPULAR:")
		p.drawCentredString(256, 706, str(sfsp[4]))
		p.line(232,704,280,704)

	#Medicamentos
	data = []

	medicamentos = [(m.medicamento.clave_farmacia,m.cantidad_surtida,m.medicamento.nombre,m.medicamento.presentacion,m.medicamento.fecha_caducidad,m.medicamento.lote) for m in ItemSolFarm.objects.filter(solfarm_id=solfarm_id)]

	styles = getSampleStyleSheet()
	styleN = styles["BodyText"]
	styleN.alignment = TA_CENTER
	styleN.fontSize = 6

	for meds in medicamentos:
		this_meds = [meds[0],meds[1],Paragraph(meds[2], styleN),meds[3],meds[4],meds[5]]
		data.append(this_meds)

	width, height = letter
								   # clave      cant       med        umed       fcad       lote
	table = Table(data, colWidths = [0.88 * cm, 0.83 * cm, 3.74 * cm, 1.02 * cm, 1.43 * cm, 1.43 * cm],
						 rowHeights = len(data) * [-0.939 * cm],)
	table.setStyle(TableStyle([
			('ALIGN', (0,0), (-1,-1), 'CENTER'), #Alineacion de las columnas
	        ('FONTSIZE', (0,0), (-1,-1), 7), #Tamaño de la fuente de la tabla
	        #('GRID', (0,1), (5,len(data)-1), 0.75, colors.black),
		]))
	table.wrapOn(p, width, height)
	table.drawOn(p, 15, 660)

	p.setFillColor(HexColor('#B6B6B6'))
	p.rect(15,688,265,12, fill=1, stroke=False)
	p.line(15,688,280,688)
	p.line(15,475,280,475)
	p.line(15,463,280,463)
	p.line(65,452,65,475)
	p.line(15,661,280,661)
	p.line(15,633,280,633)
	p.line(15,605,280,605)
	p.line(15,579,280,579)
	p.line(15,553,280,553)
	p.line(15,527,280,527)
	p.line(15,501,280,501)

	p.setFillColor(black)
	p.setFont("Helvetica-Bold", 6)
	p.drawString(17, 691, "CLAVE")
	p.drawString(43, 691, "CANT")
	p.drawString(95, 691, "MEDICAMENTO")
	p.drawString(174, 691, "U.MED")
	p.drawString(210, 691, "F.CAD")
	p.drawString(252, 691, "LOTE")

	#Datos del medico
	p.drawString(27, 466, "MÉDICO")
	p.drawString(23, 455, "SERVICIO")
	medico = [(md.medico,md.medico.servicio) for md in SolicitudFarmacia.objects.filter(pk = solfarm_id)]
	for dr in medico:
		p.drawCentredString(170, 466, str(dr[0])) #Medico
		p.drawCentredString(170, 455, str(dr[1])) #Servicio

	p.line(40,475,40,700) #clave|cant
	p.line(63,475,63,700) #cant|med
	p.line(169,475,169,700) #med|umed
	p.line(198,475,198,700) #umed|fcad
	p.line(239,475,239,700) #fcad|lote
	
	p.setFillColor(HexColor('#B6B6B6'))
	p.rect(15,436,265,16, fill=1, stroke=False)
	p.setFillColor(black)
	p.rect(15,452,265,248, fill=False, stroke=1) #Caja de grilla medicamentos
	p.setFont("Helvetica", 6)
	p.drawString(20, 445, "NOTA: LOS MEDICAMENTOS DESCRITOS SON TOTALMENTE EXCENTOS DE PAGO")
	p.drawString(20, 438, "POR ESTAR INCLUIDOS EN EL CUADRO BÁSICO DEL SEGURO POPULAR")

	#Pie de página
	p.setFont('Helvetica', 8)
	usuario = [(us.usuario, us.fecha_creacion) for us in SolicitudFarmacia.objects.filter(pk = solfarm_id)]
	for entrego in usuario:
		p.drawCentredString(60,418, str(entrego[0])) #Usuario
	p.line(20,414,100,414)
	p.setFont('Helvetica', 6)
	p.drawCentredString(60,405, "E N T R E G A")
	p.drawImage(logoSAMIH, 258,416, 15, 15, mask='auto')
	p.setFont('Helvetica', 6)
	p.drawString(256, 411, "SAMIH")
	p.setFont('Helvetica', 3)
	p.drawString(256, 408, "by DVLC")

	p.showPage()
	p.save()
	pdf = buffer.getvalue()
	buffer.close()
	response.write(pdf)
	return response
############################################################################################

#### Solicitud de Farmacia: Medicamento Controlado #################################################
class CrearSolFarmMedControladoView(FormsetMixin, CreateView):
	template_name = 'crearsolfarmmedcontrolado.html'
	model = SolicitudFarmacia
	form_class = SolicitudFarmaciaForm
	formset_class = ItemSolFarmMedControladoFormSet

	def get_context_data(self, **kwargs):
	    context = super(CrearSolFarmMedControladoView, self).get_context_data(**kwargs)
	    context['Hoy'] = datetime.now()
	    return context

	def form_valid(self, form, formset):
		form.instance.usuario = self.request.user
		form.instance.tiposol = 'medcontrolado'
		return super(CrearSolFarmMedControladoView, self).form_valid(form, formset)


class SolFarmMedControladoView(DetailView):
	template_name = 'solfarmmedcontrolado.html'
	model = SolicitudFarmacia


def PdfSolFarmMedControlaView(request, solfarm_id):
	response = HttpResponse(content_type = 'application/pdf')
	response['Content-Disposition'] = 'filename = "solfarmmedcontrolado.pdf"'

	buffer = BytesIO()

	p = canvas.Canvas(buffer, pagesize = letter)

	#Cabecera
	p.drawImage(logoHGSJR, 15,740, 120, 50, mask='auto')
	p.drawImage(logoSSA, 480,740, 120, 50, mask='auto')
	p.setFont('Helvetica', 12)
	p.drawString(195, 755, "HOSPITAL GENERAL DE SAN JUAN DEL RÍO")
	p.setFont('Helvetica-Bold', 12)
	p.drawString(225, 742, "DEPARTAMENTO DE FARMACIA")
	p.drawString(190, 730, "SALIDA DE MEDICAMENTOS CONTROLADOS")
	p.setFont('Helvetica', 10)
	solfarm = [(sf.id,sf.fecha_creacion,sf.paciente,sf.receta,sf.receta2,sf.poliza_segpop) for sf in SolicitudFarmacia.objects.filter(pk = solfarm_id)]
	for sfmc in solfarm:
		#p.setFont('Helvetica', 8)
		p.drawString(15, 713, "FOLIO:")
		p.drawCentredString(78, 713, str(sfmc[0]))
		p.line(50,711,110,711)

		p.drawString(499, 713, "FECHA:")
		fecha = datetime.strftime(sfmc[1], FORMATO_DIA) #Darle formato a la fecha
		p.drawString(542, 713, str(fecha))
		p.line(538,711,594,711)
		
		#Datos paciente
		p.drawString(15, 700, "NOMBRE DEL PACIENTE:")
		p.drawCentredString(350, 700, str(sfmc[2]))
		p.line(140,698,594,698)

		p.drawString(15, 687, "RECETA:")
		p.drawCentredString(89, 687, str(sfmc[3]))
		p.line(59,685,119,685)

		p.drawString(140, 687, "RECETA:")
		p.drawCentredString(214, 687, str(sfmc[4]))
		p.line(184,685,244,685)

		p.drawString(378,687, "PÓLIZA DE SEGURO POPULAR:")
		p.drawCentredString(564, 687, str(sfmc[5]))
		p.line(532,685,594,685)

	#Medicamentos
	data = []

	medicamentos = [(m.medicamento.clave_farmacia,m.cantidad_surtida,m.medicamento.nombre,m.medicamento.presentacion,m.medicamento.fecha_caducidad,m.medicamento.lote,m.medicamento.precio) for m in ItemSolFarm.objects.filter(solfarm_id=solfarm_id)]

	styles = getSampleStyleSheet()
	styleN = styles["BodyText"]
	styleN.alignment = TA_CENTER
	styleN.fontSize = 8

	for meds in medicamentos:
		precio_med = meds[1] * meds[6]
		this_meds = [Paragraph(meds[0], styleN), #clave
					 Paragraph(str(meds[1]), styleN), #cantidad_surtida
					 Paragraph(meds[2], styleN), #nombre
					 meds[3], #presentacion
					 meds[4], #fcad
					 meds[5], #lote
					 Paragraph("$" + str(meds[6]), styleN),	#puni
					 Paragraph("$" + str(precio_med), styleN)] #total
		data.append(this_meds)

	width, height = letter
								   # clave     cant      med        umed      fcad      lote       precio     total
	table = Table(data, colWidths = [1.2 * cm, 1 * cm, 8.7 * cm, 1.5 * cm, 2.0 * cm, 2.0 * cm, 2.0 * cm, 2.05 * cm],
						 rowHeights = len(data) * [-1.56 * cm],)
	table.setStyle(TableStyle([
			('ALIGN', (0,0), (-1,-1), 'CENTER'), #Alineacion de las columnas
	        ('FONTSIZE', (0,0), (-1,-1), 8), #Tamaño de la fuente de la tabla
	        #('GRID', (0,1), (7,len(data)-1), 0.75, colors.black),
		]))
	table.wrapOn(p, width, height)
	table.drawOn(p, 15, 625)

	p.setFillColor(HexColor('#B6B6B6'))
	p.rect(15,660,580,22, fill=1, stroke=False)
	p.rect(15,472,53,20, fill=1, stroke=False)
	p.rect(324,472,60,20, fill=1, stroke=False)
	p.line(15,660,595,660) #Encabezado
	p.line(15,625,595,625)
	p.line(15,581,595,581)
	p.line(15,537,595,537)
	p.line(68,472,68,492)
	p.line(324,472,324,492)
	p.line(384,472,384,492)
	p.line(15,492,595,492)

	p.setFillColor(black)
	p.setFont("Helvetica-Bold", 8)
	p.drawString(17, 667, "CLAVE")
	p.drawString(52, 667, "CANT")
	p.drawString(170, 667, "MEDICAMENTO")
	p.drawString(332, 667, "U.MED")
	p.drawString(383, 667, "F.CAD")
	p.drawString(440, 667, "LOTE")
	p.drawString(497, 667, "P.UNI")
	p.drawString(553, 667, "TOTAL")

	#Datos del medico
	p.drawString(27, 479, "MÉDICO")
	p.drawString(335, 479, "SERVICIO")
	medico = [(md.medico,md.medico.servicio) for md in SolicitudFarmacia.objects.filter(pk = solfarm_id)]
	for dr in medico:
		p.drawCentredString(170, 479, str(dr[0])) #Medico
		p.drawCentredString(490, 479, str(dr[1])) #Servicio

	p.line(49,492,49,682) #clave|cant
	p.line(77,492,77,682) #cant|med
	p.line(324,492,324,682) #med|umed
	p.line(367,492,367,682) #umed|fcad
	p.line(423,492,423,682) #fcad|lote
	p.line(480,492,480,682) #lote|puni
	p.line(536,492,536,682) #puni|total
	p.setFillColor(black)
	p.rect(15,472,580,210, fill=False, stroke=1) #Caja de grilla medicamentos

	#Pie de página
	p.setFont('Helvetica-Bold', 8)
	p.drawCentredString(110,430, "QFB SILVIA V. GALLARDO GARCÍA")
	p.line(20,426,200,426)
	p.setFont('Helvetica', 6)
	p.drawCentredString(110,447, "E N T R E G A")
	p.drawCentredString(110,417, "RESPONSABLE DE FARMACIA")
	p.drawImage(logoSAMIH, 575,428, 15, 15, mask='auto')
	p.setFont('Helvetica', 6)
	p.drawString(573, 423, "SAMIH")
	p.setFont('Helvetica', 3)
	p.drawString(573, 420, "by DVLC")

	p.showPage()
	p.save()
	pdf = buffer.getvalue()
	buffer.close()
	response.write(pdf)
	return response
from os import path, mkdir

from ReportesPDFContravel import ReportesPDFContravel
from django.http import HttpResponse  ## eventualmente lo podremos quitar
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.contrib import messages

from .models import TipoReporte, EjecucionReporte, VariablesUltimoReporte, MesReporte


##from django.http import Http404
##from django.template import loader

# Create your views here.

class ReporteView(generic.DetailView):
    model = EjecucionReporte
    template_name = 'reportesVC/detalleReporte.html'

'''
### Used before
def index0(request):
    tipos_reportes = TipoReporte.objects.order_by('-id')[:5]
    template = loader.get_template('reportesVC/index.html')
    context = {
        'tipos_reportes': tipos_reportes,
    }
    ##return HttpResponse("Bienvenido a la página de reportes de Contravel!")
    return HttpResponse(template.render(context, request))
'''

def index(request):
    tiposReportes = TipoReporte.objects.order_by('-id')[:5]
    context = {
        'tipos_reportes': tiposReportes,
    }
    return render(request, 'reportesVC/index.html', context)

def reportes(request, tipoNombre,status):
    tipo = TipoReporte.objects.get(nombre=tipoNombre)
    variablesUltimoReporte = VariablesUltimoReporte.objects.all()
    return render(request, 'reportesVC/ejecutarReporte.html', {'tipo_nombre':tipoNombre, 'tipo_valor':tipo.id, 'variables_ultimo_reporte':variablesUltimoReporte, 'status':status})

'''
### Used before
def reporteVentas0(request, reporte_id):
    try:
        reporte = EjecucionReporte.objects.get(pk=reporte_id)
    except EjecucionReporte.DoesNotExist:
        raise Http404("El reporte no existe!")
    return render(request, 'reportesVC/detalleReporte.html', {'reporte': reporte, 'reporte_id':reporte_id})
    ###return HttpResponse("Página del reporte de Ventas: " + reporte_id)
'''

def reporte(request, tipoNombre, reporteId):
    reporte = get_object_or_404(EjecucionReporte, pk=reporteId) ##tambien existe get_list_or_404() 
    return render(request, 'reportesVC/detalleReporte.html', {'reporte': reporte})
    ###return HttpResponse("Página del reporte de Ventas: " + reporte_id)

def creaReporte(request, tipoNombre, status):
    ###Primero guardo valores en la tabla de variables
    variables = {}
    ##res = True

    vUR = VariablesUltimoReporte.objects.all()
    for var in vUR:
        if var.editable:
            var.valor = request.POST[str(var.id) + "_" + var.nombre]
        var.save()
        variables[var.nombre] = var.valor

    ###Despues guardo con status iniciando ejecución en ejecucionreporte con nombre y ruta del archivo
    reporte = EjecucionReporte()
    reporte.tipoReporte=TipoReporte.objects.get(pk=variables["TIPO REPORTE"])
    reporte.mesPeriodo=MesReporte.objects.get(pk=variables["MES"])
    reporte.semana=variables["SEMANA"]
    reporte.anoPeriodo=variables["AÑO"]
    reporte.diaIniciaPeriodo=variables["DIA INICIAL PERIODO"]
    reporte.diaFinPeriodo=variables["DIA FINAL PERIODO"]
    reporte.fechaEjecucion=timezone.now()
    reporte.estatus = "Iniciandos"
    reporte.nombreArchivo = variables['NOMBRE ARCHIVO']
    reporte.rutaArchivo = "reportesContravel/reportesVC/archivos/" + tipoNombre + "/"
    reporte.save()

    ###Por último, ejecuto reporte
    rep = ReportesPDFContravel(reporte.semana, reporte.anoPeriodo, reporte.mesPeriodo.nombre, reporte.diaIniciaPeriodo, reporte.diaFinPeriodo, reporte.nombreArchivo, reporte.rutaArchivo, reporte.tipoReporte.nombre)
    ##if(reporte.tipoReporte.id == 1):
        ##cant = rep.createReportVentas()
    ##elif(reporte.tipoReporte.id == 2):
        ##cant = rep.createReportComisiones()
    cant = rep.createReport()

    if cant > 0:
       reporte.estatus = reporte.estatus = "Creados" + str(cant)
       reporte.save()

    ###Actualizo linea a ejecucion reporte, con informacion del zip
    reporte.nombreZip = rep.createZip()
    reporte.save()

    if len(rep.mensajesErr)>0:
        ##messages.info(request, "Error en el Cliente: " + " -> " + rep.nomCliente)
        for mensajesErr in sorted(rep.mensajesErr.keys()):
            if rep.mensajesErr[mensajesErr]["tipo"]=="debug":
                messages.debug(request, rep.mensajesErr[mensajesErr]["mensaje"])
            if rep.mensajesErr[mensajesErr]["tipo"] == "info":
                messages.info(request, rep.mensajesErr[mensajesErr]["mensaje"])
            if rep.mensajesErr[mensajesErr]["tipo"] == "success":
                messages.success(request, rep.mensajesErr[mensajesErr]["mensaje"])
            if rep.mensajesErr[mensajesErr]["tipo"] == "warning":
                messages.warning(request, rep.mensajesErr[mensajesErr]["mensaje"])
            if rep.mensajesErr[mensajesErr]["tipo"] == "error":
                messages.error(request, rep.mensajesErr[mensajesErr]["mensaje"])

        return HttpResponseRedirect(reverse('reportesVC:reportes', kwargs={'tipoNombre': tipoNombre, 'status': status}))

    else:
        ###Por último muestro resultado
        ### con HttpResponseRedirect evito que se de doble click y se vuelva a ejecutar
        ### con reverse recontruyo la URL
        return HttpResponseRedirect(reverse('reportesVC:reporte', kwargs={'tipoNombre': tipoNombre, 'pk': reporte.id}))




def subirArchivo(request, tipoNombre, status):
    status = "Error"
    ##tipo = TipoReporte.objects.get(nombre=tipoNombre)
    if request.method == 'POST':
        fileName = str(request.FILES["myfile"])
        rutaArchivo = "/root/vep35/reportesContravel/reportesVC/archivos/" + tipoNombre + "/"
        handle_uploaded_file(request.FILES["myfile"], fileName, rutaArchivo)
        status = "Subido"
        vURfileName = VariablesUltimoReporte.objects.get(pk=7)
        vURfileName.valor=fileName
        vURfileName.save()
    return HttpResponseRedirect(reverse('reportesVC:reportes', kwargs={'tipoNombre':tipoNombre, 'status':status}))
 
def handle_uploaded_file(file, filename, rutaArchivo):
    if not path.exists(rutaArchivo):
        mkdir(rutaArchivo)
 
    with open(rutaArchivo + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

def descargarZip(request, tipoNombre, pk):
    reporte = get_object_or_404(EjecucionReporte, pk=pk)
    filePath = reporte.rutaArchivo + reporte.nombreZip
    fsock = open(filePath,"rb")
    print("abrio")
    response = HttpResponse(fsock, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=' + reporte.tipoReporte.nombre  + 'ReportesS' + reporte.semana + reporte.anoPeriodo + '.zip'
    return response

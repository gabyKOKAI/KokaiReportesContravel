from os import path, mkdir

from ReportesPDFContravel import ReportesPDFContravel
from ComisionesContravel import ComisionesContravel
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

### Global Variables
###servidor
##dirArchivos =  "/home/kokaiweb/vep35/reportesContravel/reportesContravel/reportesVC/archivos/"
###desarrollo
dirArchivos = "reportesContravel/reportesVC/archivos/"

# Create your views here.

class ReporteView(generic.DetailView):
    model = EjecucionReporte
    template_name = 'reportesVC/detalleReporte.html'

class CalculoView(generic.DetailView):
    model = EjecucionReporte
    template_name = 'reportesVC/detalleCalculo.html'
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

def reportes(request, tipoNombre, status):
    tipo = TipoReporte.objects.get(nombre=tipoNombre)
    variablesUltimoReporte = VariablesUltimoReporte.objects.all()
    return render(request, 'reportesVC/ejecutarReporte.html', {'tipo_nombre':tipoNombre, 'tipo_valor':tipo.id, 'tipo_nombre_largo':tipo.nombreLargo, 'variables_ultimo_reporte':variablesUltimoReporte, 'status':status})


def calculos(request, tipoNombre, status):
    tipo = TipoReporte.objects.get(nombre=tipoNombre)
    variablesUltimoReporte = VariablesUltimoReporte.objects.all()
    return render(request, 'reportesVC/ejecutarCalculo.html', {'tipo_nombre':tipoNombre, 'tipo_valor':tipo.id, 'tipo_nombre_largo':tipo.nombreLargo, 'variables_ultimo_reporte':variablesUltimoReporte, 'status':status})

def conciliaciones(request, tipoNombre, status):
    tipo = TipoReporte.objects.get(nombre=tipoNombre)
    variablesUltimoReporte = VariablesUltimoReporte.objects.all()
    return render(request, 'reportesVC/conciliaciones.html', {'tipo_nombre':tipoNombre, 'tipo_valor':tipo.id, 'tipo_nombre_largo':tipo.nombreLargo, 'variables_ultimo_reporte':variablesUltimoReporte, 'status':status})


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

### actualiza valores en table de variebles
def actualizaValores(request):
    variables = {}

    vUR = VariablesUltimoReporte.objects.all()
    for var in vUR:
        if var.editable:
            var.valor = request.POST[str(var.id) + "_" + var.nombre]
        var.save()
        variables[var.nombre] = var.valor

    ##print(variables)
    return variables

### Guardo con status iniciando ejecución en ejecucionreporte con nombre y ruta del archivo
def guardaHistorial(variables, tipoNombre):
    reporte = EjecucionReporte()
    reporte.tipoReporte = TipoReporte.objects.get(pk=variables["TIPO REPORTE"])
    reporte.mesPeriodo = MesReporte.objects.get(pk=variables["MES"])
    reporte.semana = variables["SEMANA"]
    reporte.anoPeriodo = variables["AÑO"]
    reporte.diaIniciaPeriodo = variables["DIA INICIAL PERIODO"]
    reporte.diaFinPeriodo = variables["DIA FINAL PERIODO"]
    reporte.fechaEjecucion = timezone.now()
    reporte.estatus = "Iniciandos"
    reporte.nombreArchivo = variables['NOMBRE ARCHIVO']
    reporte.rutaArchivo = dirArchivos + tipoNombre + "/"
    reporte.save()
    return reporte

### Get Error and Success messages
def getMessages(request, mensajes):
    for mensajesErr in sorted(mensajes.keys()):
        if mensajes[mensajesErr]["tipo"] == "debug":
            messages.debug(request, mensajes[mensajesErr]["mensaje"])
        if mensajes[mensajesErr]["tipo"] == "info":
            messages.info(request, mensajes[mensajesErr]["mensaje"])
        if mensajes[mensajesErr]["tipo"] == "success":
            messages.success(request, mensajes[mensajesErr]["mensaje"])
        if mensajes[mensajesErr]["tipo"] == "warning":
            messages.warning(request, mensajes[mensajesErr]["mensaje"])
        if mensajes[mensajesErr]["tipo"] == "error":
            messages.error(request, mensajes[mensajesErr]["mensaje"])

def creaReporte(request, tipoNombre, status):
    variables = {}

    ###Primero guardo valores en la tabla de variables
    variables = actualizaValores(request)
    
    ###Despues guardo con status iniciando ejecución en ejecucionreporte con nombre y ruta del archivo
    reporte = guardaHistorial(variables, tipoNombre)

    ###Por último, ejecuto reporte
    rep = ReportesPDFContravel(reporte.semana, reporte.anoPeriodo, reporte.mesPeriodo.nombre, reporte.diaIniciaPeriodo, reporte.diaFinPeriodo, reporte.nombreArchivo, reporte.rutaArchivo, reporte.tipoReporte.nombre)

    mylist = request.POST.getlist('CBtipoReporte')
    if 'reporteNuevo' in mylist:
        cant = rep.createReport("new")
    elif 'reporteViejo' in mylist:
        cant = rep.createReport("old")

    ###Actualizo status del historial de reportes
    if cant > 0:
       reporte.estatus = "Creado" + str(cant)
       reporte.save()

    ###Creo Zip y Actualizo linea a ejecucion reporte, con informacion del zip
    reporte.nombreZip = rep.createZip()
    reporte.save()

    ##print(rep.mensajesErr)
    if len(rep.mensajesErr)>0:
        getMessages(request, rep.mensajesErr)
        return HttpResponseRedirect(reverse('reportesVC:reportes', kwargs={'tipoNombre': tipoNombre, 'status': status}))

    else:
        ###Por último muestro resultado
        ### con HttpResponseRedirect evito que se de doble click y se vuelva a ejecutar
        ### con reverse recontruyo la URL
        messages.success(request, "La creación de reportes se ejecuto correctamente!")
        return HttpResponseRedirect(reverse('reportesVC:reporte', kwargs={'tipoNombre': tipoNombre, 'pk': reporte.id}))

def handle_uploaded_file(file, filename, rutaArchivo):
    if not path.exists(rutaArchivo):
        mkdir(rutaArchivo)

    with open(rutaArchivo + filename, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

def subirArch(request, fileName, tipoNombre):
    try:
        if(fileName==""):
            fileName = str(request.FILES["myfile"])
        rutaArchivo = dirArchivos + tipoNombre + "/"
        handle_uploaded_file(request.FILES["myfile"], fileName, rutaArchivo)
        messages.success(request, "El archivo se subio con exito!!!")
    except Exception as err:
        messages.error(request,"Favor de seleccionar un archivo para subir.")
        fileName = "error"
    return fileName

def actualizaFileName(fileName):
    vURfileName = VariablesUltimoReporte.objects.get(pk=7)
    vURfileName.valor = fileName
    vURfileName.save()
    return

def subirArchivo(request, tipoNombre, status):
    status = "Error"
    if request.method == 'POST':
        fileName = subirArch(request,"",tipoNombre)
        if fileName != "error":
            status = "Subido"
        else:
            status = "Error"
        actualizaFileName(fileName)
    return HttpResponseRedirect(reverse('reportesVC:reportes', kwargs={'tipoNombre':tipoNombre, 'status':status}))

def subirArchivoCal(request, tipoNombre, status):
    status = "Error"
    if request.method == 'POST':
        mylist = request.POST.getlist('CBtipoArchivo')
        newFileName = ""
        if 'archivoExcepciones' in mylist:
            newFileName = "CodClienteAeroCom.csv"
        elif 'archivoMex' in mylist:
            newFileName = "CodIATAMex.csv"
        elif 'archivoEua' in mylist:
            newFileName = "CodIATAEua.csv"
        elif 'archivoCan' in mylist:
            newFileName = "CodIATACan.csv"
    if 'subeArchivo' in request.POST:
        fileName = subirArch(request, newFileName , tipoNombre)
        if 'archivoCsv' in mylist:
            actualizaFileName(fileName)
            status = "Subido"
        else:
            status = "SubidoConf"
        if fileName == "error":
            status = "Error"
        return HttpResponseRedirect(reverse('reportesVC:calculos', kwargs={'tipoNombre': tipoNombre, 'status': status}))
    elif 'bajaArchivo' in request.POST:
        if 'archivoCsv' not in mylist:
            rutaArchivo = dirArchivos + tipoNombre + "/"
            filePath = rutaArchivo + newFileName
            fsock = open(filePath, "rb")
            response = HttpResponse(fsock, content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename=' + newFileName
            status = "Bajado"
            ##messages.success(request, "Archivo descargado correctamente.")
            return response
        else:
            messages.warning(request, "No es posible descargar este archivo, seleccione otra opción.")
            return HttpResponseRedirect(reverse('reportesVC:calculos', kwargs={'tipoNombre': tipoNombre, 'status': status}))
    else:
        messages.warning(request, "No dio click en ninguna opción valida")
        return HttpResponseRedirect(reverse('reportesVC:calculos', kwargs={'tipoNombre': tipoNombre, 'status': status}))

def descargarZip(request, tipoNombre, pk):
    reporte = get_object_or_404(EjecucionReporte, pk=pk)
    filePath = reporte.rutaArchivo + reporte.nombreZip
    fsock = open(filePath,"rb")
    ##print("abrio")
    response = HttpResponse(fsock, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=' + reporte.tipoReporte.nombreLargo  + 'ReportesS' + reporte.semana + reporte.anoPeriodo + '.zip'
    return response

def descargarFile(request, tipoNombre, pk):
    reporte = get_object_or_404(EjecucionReporte, pk=pk)
    filePath = reporte.rutaArchivo + reporte.nombreZip
    fsock = open(filePath,"rb")
    ## print("abrio1")
    response = HttpResponse(fsock, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=' + reporte.tipoReporte.nombreLargo + reporte.nombreZip
    return response

def ejecutaComisiones(request, tipoNombre, status):
    variables = {}

    ###Primero guardo valores en la tabla de variables
    variables = actualizaValores(request)

    ###Despues guardo con status iniciando ejecución en ejecucionreporte con nombre y ruta del archivo
    reporte = guardaHistorial(variables, tipoNombre)

    ###Por último, ejecuto reporte
    calCom = ComisionesContravel(reporte.semana, reporte.anoPeriodo, reporte.mesPeriodo.nombre, reporte.nombreArchivo, reporte.rutaArchivo,
                               reporte.tipoReporte.nombre)

    nomArchivoNew = calCom.createReportPorComisiones()

    ###Actualizo status del historial de reportes
    if nomArchivoNew != "":
        reporte.estatus = "Calculado"
        reporte.save()

    ###Creo Zip y Actualizo linea a ejecucion reporte, con informacion del zip
    reporte.nombreZip = nomArchivoNew
    reporte.save()

    if len(calCom.mensajesErr) > 0:
        getMessages(request, calCom.mensajesErr)
        return HttpResponseRedirect(reverse('reportesVC:calculos', kwargs={'tipoNombre': tipoNombre, 'status': status}))

    else:
        ###Por último muestro resultado
        ### con HttpResponseRedirect evito que se de doble click y se vuelva a ejecutar
        ### con reverse recontruyo la URL
        messages.success(request, "El calculo de comisiones se ejecuto correctamente!")
        return HttpResponseRedirect(reverse('reportesVC:calculo', kwargs={'tipoNombre': tipoNombre, 'pk': reporte.id}))
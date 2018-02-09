from os import path, mkdir

from ClasesGenericas import ManageFiles
from ReportesPDFContravel import ReportesPDFContravel
from ComisionesContravel import ComisionesContravel
from Conciliador import Conciliador
from ConciliadorSAT import ConciliadorSAT
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse  ## eventualmente lo podremos quitar
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic
from django.contrib import messages
from django.contrib import auth
import datetime

from .models import TipoReporte, EjecucionReporte, VariablesUltimoReporte, MesReporte, ActualizacionesArchivos

##from django.http import Http404
##from django.template import loader

### Global Variables
###servidor
dirArchivos = "/home/kokaiweb/vep35/reportesContravel/reportesContravel/reportesVC/archivos/"


###desarrollo
##dirArchivos = "reportesContravel/reportesVC/archivos/"

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

@login_required
def index(request):
    tiposReportes = TipoReporte.objects.order_by('-id')[:5]
    context = {
        'tipos_reportes': tiposReportes,
    }
    return render(request, 'reportesVC/index.html', context)

##@login_required
@permission_required('reportesVC.can_run_Report')
def reportes(request, tipoNombre, status):
    tipo = TipoReporte.objects.get(nombre=tipoNombre)
    variablesUltimoReporte = VariablesUltimoReporte.objects.all()
    return render(request, 'reportesVC/ejecutarReporte.html',
                  {'tipo_nombre': tipoNombre, 'tipo_valor': tipo.id, 'tipo_nombre_largo': tipo.nombreLargo,
                   'variables_ultimo_reporte': variablesUltimoReporte, 'status': status})

@permission_required('reportesVC.can_run_AdminConta')
def adminConta(request):
    listaLogConta = ActualizacionesArchivos.objects.all()
    return render(request, 'conta/adminConta.html',{'lista_log_conta':listaLogConta})

@login_required
@permission_required('reportesVC.can_run_Calculos')
def calculos(request, tipoNombre, status):
    tipo = TipoReporte.objects.get(nombre=tipoNombre)
    variablesUltimoReporte = VariablesUltimoReporte.objects.all()
    return render(request, 'reportesVC/ejecutarCalculo.html',
                  {'tipo_nombre': tipoNombre, 'tipo_valor': tipo.id, 'tipo_nombre_largo': tipo.nombreLargo,
                   'variables_ultimo_reporte': variablesUltimoReporte, 'status': status})

@login_required
@permission_required('reportesVC.can_run_Conciliacion')
def conciliacionBancos(request, tipoNombre, status):
    tipo = TipoReporte.objects.get(nombre=tipoNombre)
    return render(request, 'conta/conciliacionBancos.html',
                  {'tipo_nombre': tipoNombre, 'tipo_valor': tipo.id, 'tipo_nombre_largo': tipo.nombreLargo,
                   'status': status})

@login_required
@permission_required('reportesVC.can_run_Conciliacion')
def conciliacionSAT(request, tipoNombre, status):
    tipo = TipoReporte.objects.get(nombre=tipoNombre)
    return render(request, 'conta/conciliacionSAT.html',
                  {'tipo_nombre': tipoNombre, 'tipo_valor': tipo.id, 'tipo_nombre_largo': tipo.nombreLargo,
                    'status': status})

@login_required
@permission_required('reportesVC.can_run_Conciliacion')
def conciliacionIngresos(request, tipoNombre, status):
    tipo = TipoReporte.objects.get(nombre=tipoNombre)
    return render(request, 'conta/conciliacionIngresos.html',
                  {'tipo_nombre': tipoNombre, 'tipo_valor': tipo.id, 'tipo_nombre_largo': tipo.nombreLargo,
                    'status': status})

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

@login_required
def reporte(request, tipoNombre, reporteId):
    reporte = get_object_or_404(EjecucionReporte, pk=reporteId)  ##tambien existe get_list_or_404()
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
def guardaHistorial(variables, tipoNombre, request):
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
    reporte.user = request.user
    
    reporte.save()
    return reporte


### Guardo con status iniciando ejecución en ejecucionreporte con nombre y ruta del archivo
def guardaActuArch(tipoNombre, nombreArchivo, status, request):
    actArch = ActualizacionesArchivos()
    actArch.tipoReporte = TipoReporte.objects.get(nombre=tipoNombre)
    actArch.estatus = status
    actArch.nombreArchivo = nombreArchivo[-50:]
    actArch.user = request.user
    actArch.save()
    return actArch


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


@login_required
@permission_required('reportesVC.can_run_Report')
def creaReporte(request, tipoNombre, status):
    variables = {}

    ###Primero guardo valores en la tabla de variables
    variables = actualizaValores(request)

    ###Despues guardo con status iniciando ejecución en ejecucionreporte con nombre y ruta del archivo
    reporte = guardaHistorial(variables, tipoNombre, request)

    ###Por último, ejecuto reporte
    rep = ReportesPDFContravel(reporte.semana, reporte.anoPeriodo, reporte.mesPeriodo.nombre, reporte.diaIniciaPeriodo,
                               reporte.diaFinPeriodo, reporte.nombreArchivo, reporte.rutaArchivo,
                               reporte.tipoReporte.nombre)

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
    mf = ManageFiles.ManageFiles()

    reporte.nombreZip = mf.createZip(reporte.rutaArchivo + "ReportesS" + rep.semana + rep.ano + "//", reporte.rutaArchivo, "ReportesS" + rep.semana + rep.ano)
    reporte.save()

    ##print(rep.mensajesErr)
    if len(rep.wriErr.mensajesErr) > 0:
        getMessages(request, rep.wriErr.mensajesErr)
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

def subirArch(request, fileName, tipoNombre, subFoldr):
    try:
        if (fileName == ""):
            fileName = str(request.FILES["myfile"])
        rutaArchivo = dirArchivos + tipoNombre + "/" + subFoldr
        ##print(rutaArchivo)
        handle_uploaded_file(request.FILES["myfile"], fileName, rutaArchivo)
        messages.success(request, "El archivo se subio con exito!!!")
    except Exception as err:
        messages.error(request, "Favor de seleccionar un archivo para subir." + str(err))
        fileName = "error"
    return fileName

def bajarArch(request,fileName,newFileName):
    try:
        ##print(fileName)
        if(path.isfile(fileName)):
            ##print("bajando " + fileName)
            fsock = open(fileName, "rb")
            response = HttpResponse(fsock, content_type='application/force-download')
            response['Content-Disposition'] = 'attachment; filename=' + newFileName
            ##messages.success(request, "El archivo se descargo con exito!!!")
        else:
            messages.error(request, "No existe el archivo para descargar")
            response = "error"
    except Exception as err:
        messages.error(request, "Error al descargar archivo")
        response = "error"
    return response

def actualizaFileName(fileName):
    ##print(fileName)
    vURfileName = VariablesUltimoReporte.objects.get(pk=7)
    vURfileName.valor = fileName
    vURfileName.save()
    return

@login_required
def subirArchivo(request, tipoNombre, status):
    status = "Error"
    if request.method == 'POST':
        fileName = subirArch(request, "", tipoNombre,"")
        if fileName != "error":
            status = "Subido"
        else:
            status = "Error"
        actualizaFileName(fileName)
    return HttpResponseRedirect(reverse('reportesVC:reportes', kwargs={'tipoNombre': tipoNombre, 'status': status}))

@login_required
@permission_required('reportesVC.can_run_Calculos')
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
        fileName = subirArch(request, newFileName, tipoNombre,"")
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
            return HttpResponseRedirect(
                reverse('reportesVC:calculos', kwargs={'tipoNombre': tipoNombre, 'status': status}))
    else:
        messages.warning(request, "No dio click en ninguna opción valida")
        return HttpResponseRedirect(reverse('reportesVC:calculos', kwargs={'tipoNombre': tipoNombre, 'status': status}))

def regresaFileNameConc(request, agencia):
    status = "Error"
    if request.method == 'POST':
        mylist = request.POST.getlist('CBtipoArchivo')
        newFileName = ""
        if 'archivoSaldos' in mylist:
            newFileName = "Saldos " + agencia + ".csv"
        elif 'archivoBancos' in mylist:
            newFileName = "Bancos " + agencia + ".csv"
        elif 'archivoAuxiliar' in mylist:
            newFileName = "ICAAV " + agencia + ".csv"
        elif 'archivoDiarios' in mylist:
            newFileName = "Diarios" + agencia + ".csv"
        elif 'archivoSAT' in mylist:
            newFileName = "SAT " + agencia + ".csv"
        elif 'archivoNomina' in mylist:
            newFileName = "Nomina " + agencia + ".csv"
        elif 'archivoVentas' in mylist:
            newFileName = "Ventas " + agencia + ".csv"
    return newFileName

@login_required
@permission_required('reportesVC.can_run_Conciliacion')
def subirArchivoCon(request, tipoNombre, status):
    status = "Error"
    if request.method == 'POST':
        agencia = str(request.POST.getlist('CBAgencia')[0])
        newFileName = regresaFileNameConc(request, agencia)
        fecha = str(request.POST.getlist('DATEreportes')[0])
        if (fecha == ''):
            fecha = datetime.datetime.today().strftime('%Y-%m-%d')
            ##print("fecha" + fecha)
        subFolder =  fecha[2:4] + "-" + fecha[5:7] + "/"

    if 'subeArchivo' == str(request.POST.getlist('boton')[0]):
        fileName = subirArch(request, newFileName, tipoNombre, subFolder)
        guardaActuArch(tipoNombre, fileName, "subioArch", request)
        status = "Subido"
        if fileName == "error":
            status = "Error"
        if "SAT" in tipoNombre:
            return HttpResponseRedirect(reverse('reportesVC:conciliacionSAT', kwargs={'tipoNombre': tipoNombre, 'status': status}))
        elif "Bancos" in tipoNombre:
            return HttpResponseRedirect(
                    reverse('reportesVC:conciliacionBancos', kwargs={'tipoNombre': tipoNombre, 'status': status}))
        elif "Ingresos" in tipoNombre:
            return HttpResponseRedirect(
                    reverse('reportesVC:conciliacionIngresos', kwargs={'tipoNombre': tipoNombre, 'status': status}))
    elif 'bajaArchivo' == str(request.POST.getlist('boton')[0]):
        fileName = dirArchivos + tipoNombre + "/" + subFolder + newFileName
        response = bajarArch(request, fileName , newFileName)
        guardaActuArch(tipoNombre, fileName, "bajoArch", request)
        status = "Bajado"
        if(str(response) == "error"):
            status = "Error"
            if "SAT" in tipoNombre:
                return HttpResponseRedirect(
                    reverse('reportesVC:conciliacionSAT', kwargs={'tipoNombre': tipoNombre, 'status': status}))
            elif "Bancos" in tipoNombre:
                return HttpResponseRedirect(
                    reverse('reportesVC:conciliacionBancos', kwargs={'tipoNombre': tipoNombre, 'status': status}))
            elif "Ingresos" in tipoNombre:
                return HttpResponseRedirect(
                    reverse('reportesVC:conciliacionIngresos', kwargs={'tipoNombre': tipoNombre, 'status': status}))
        return response
    else:
        messages.warning(request, "No dio click en ninguna opción valida")
        return HttpResponseRedirect(reverse('reportesVC:calculos', kwargs={'tipoNombre': tipoNombre, 'status': status}))

@login_required
def descargarZip(request, tipoNombre, pk):
    reporte = get_object_or_404(EjecucionReporte, pk=pk)
    filePath = reporte.rutaArchivo + reporte.nombreZip
    fsock = open(filePath, "rb")
    ##print("abrio")
    response = HttpResponse(fsock, content_type='application/zip')
    response[
        'Content-Disposition'] = 'attachment; filename=' + reporte.tipoReporte.nombreLargo + 'ReportesS' + reporte.semana + reporte.anoPeriodo + '.zip'
    return response

@login_required
def descargarFile(request, tipoNombre, pk):
    reporte = get_object_or_404(EjecucionReporte, pk=pk)
    filePath = reporte.rutaArchivo + reporte.nombreZip
    fsock = open(filePath, "rb")
    ## print("abrio1")
    response = HttpResponse(fsock, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=' + reporte.tipoReporte.nombreLargo + reporte.nombreZip
    return response

@login_required
def descargarRepCXC(request, tipoNombre, pk):
    reporte = get_object_or_404(EjecucionReporte, pk=pk)
    filePath = reporte.rutaArchivo + "ReporteCXC" + reporte.semana + ".csv"
    fsock = open(filePath, "rb")
    ## print("abrio1")
    response = HttpResponse(fsock, content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename=' + "ReporteCXC" + reporte.semana + ".csv"
    return response

@login_required
@permission_required('reportesVC.can_run_Calculos')
def ejecutaComisiones(request, tipoNombre, status):
    variables = {}

    ###Primero guardo valores en la tabla de variables
    variables = actualizaValores(request)

    ###Despues guardo con status iniciando ejecución en ejecucionreporte con nombre y ruta del archivo
    reporte = guardaHistorial(variables, tipoNombre, request)

    ###Por último, ejecuto reporte
    calCom = ComisionesContravel(reporte.semana, reporte.anoPeriodo, reporte.mesPeriodo.nombre, reporte.nombreArchivo,
                                 reporte.rutaArchivo,
                                 reporte.tipoReporte.nombre)

    nomArchivoNew = calCom.createReportPorComisiones()

    ###Actualizo status del historial de reportes
    if nomArchivoNew != "":
        reporte.estatus = "Calculado"
        reporte.save()

    ###Creo Zip y Actualizo linea a ejecucion reporte, con informacion del zip
    reporte.nombreZip = nomArchivoNew
    reporte.save()

    if len(calCom.wriErr.mensajesErr) > 0:
        getMessages(request, calCom.wriErr.mensajesErr)
        return HttpResponseRedirect(reverse('reportesVC:calculos', kwargs={'tipoNombre': tipoNombre, 'status': status}))

    else:
        ###Por último muestro resultado
        ### con HttpResponseRedirect evito que se de doble click y se vuelva a ejecutar
        ### con reverse recontruyo la URL
        messages.success(request, "El calculo de comisiones se ejecuto correctamente!")
        return HttpResponseRedirect(reverse('reportesVC:calculo', kwargs={'tipoNombre': tipoNombre, 'pk': reporte.id}))

@login_required
@permission_required('reportesVC.can_run_Conciliacion')
def conciliaBancos(request, tipoNombre, status):
    if 'conciliar' == str(request.POST.getlist('boton')[0]):
        ##print("entre")
        variables = {}
        ##print(str(request.POST.getlist('CBAgencia')))
        agencia = str(request.POST.getlist('CBAgencia')[0])
        fecha = str(request.POST.getlist('DATEreportes')[0])
        if (fecha == ''):
            fecha = datetime.datetime.today().strftime('%Y-%m-%d')
            ##print("fecha" + fecha)
        subFolder = fecha[2:4] + "-" + fecha[5:7] + "/"

        ###Primero guardo valores en la tabla de variables
        ##variables = actualizaValores(request)

        ###Despues guardo con status iniciando ejecución en ejecucionreporte con nombre y ruta del archivo
        ##reporte = guardaHistorial(variables, tipoNombre, request)

        ###Por último, ejecuto reporte
        ##agencia = "Contravel"
        dirConc = dirArchivos + tipoNombre + "/"
        conci = Conciliador(agencia, fecha,dirConc, subFolder)

        ### Conciliacion Bancos/ICAAV
        conci.extractInfo()
        if(len(conci.wriErr.mensajesErr) == 0):
            conci.recorreBanco()
            conci.recorreICAAV()
            conci.recorreResCorto2()

        ###Actualizo status del historial de reportes
        ##if nomArchivoNew != "":
            ##reporte.estatus = "Calculado"
            ##reporte.save()

        ###Creo Zip y Actualizo linea a ejecucion reporte, con informacion del zip
        ##reporte.nombreZip = conci.createZip()
        ##reporte.save()

        if len(conci.wriErr.mensajesErr) > 0:
            getMessages(request, conci.wriErr.mensajesErr)
            return HttpResponseRedirect(reverse('reportesVC:conciliacionBancos', kwargs={'tipoNombre': tipoNombre, 'status': status}))

        else:
            ###Por último muestro resultado
            ### con HttpResponseRedirect evito que se de doble click y se vuelva a ejecutar
            ### con reverse recontruyo la URL
            guardaActuArch(tipoNombre, agencia + "-" + fecha, "concilio", request)
            status="ok"
            ##messages.success(request, "La conciliación se ejecuto correctamente!")
            mf = ManageFiles.ManageFiles()
            filePath = dirConc + subFolder + fecha[8:] + "/" + agencia + "/"
            fileName = agencia + fecha[:4] + fecha[5:7] + fecha[8:]
            nombreZip = mf.createZip(filePath, dirConc, fileName)
            fsock = open(dirConc + nombreZip, "rb")
            response = HttpResponse(fsock, content_type='application/zip')
            response[
                'Content-Disposition'] = 'attachment; filename=' + fileName + '.zip'
            return response
            ##return HttpResponseRedirect(
                ##reverse('reportesVC:conciliaciones', kwargs={'tipoNombre': tipoNombre, 'status': status}))
    elif('bajaArchivo' == str(request.POST.getlist('boton')[0]) or 'subeArchivo' == str(request.POST.getlist('boton')[0])):
        return subirArchivoCon(request, tipoNombre, status)
    else:
        return HttpResponseRedirect(
            reverse('reportesVC:conciliacionBancos', kwargs={'tipoNombre': tipoNombre, 'status': status}))


@login_required
@permission_required('reportesVC.can_run_Conciliacion')
def conciliaSAT(request, tipoNombre, status):
        if 'conciliar' == str(request.POST.getlist('boton')[0]):
            ##print("entre")
            variables = {}
            ##print(str(request.POST.getlist('CBAgencia')))
            agencia = str(request.POST.getlist('CBAgencia')[0])
            ano = str(request.POST.getlist('InpAno')[0])
            if (ano == ''):
                ano = datetime.datetime.today().strftime('%y')
                ##print("ano" + ano)
            mesesAux = request.POST.getlist('CBMes')
            meses = []
            for mesStr in mesesAux:
                meses.append(int(mesStr))
            ##print(meses)
            if(meses == []):
                meses.append(int(datetime.datetime.today().strftime('%m')))
            ###Ejecuto reporte
            dirConc = dirArchivos + tipoNombre + "/"
            conciSAT = ConciliadorSAT(agencia, dirConc, meses,ano)

            ### Conciliacion SAT/ICAAV
            conciSAT.extractInfoDiarios()
            conciSAT.extractInfoSAT()
            conciSAT.extractInfoNomina()

            if (len(conciSAT.wriErr.mensajesErr) == 0):
                filePath = conciSAT.recorreResDiariosSATIcaav()
            if len(conciSAT.wriErr.mensajesErr) > 0:
                print("entre aqui errores!!!")
                print(str(conciSAT.wriErr.mensajesErr))
                getMessages(request, conciSAT.wriErr.mensajesErr)
                return HttpResponseRedirect(
                    reverse('reportesVC:conciliacionSAT', kwargs={'tipoNombre': tipoNombre, 'status': status}))

            else:
                ###Por último muestro resultado
                ### con HttpResponseRedirect evito que se de doble click y se vuelva a ejecutar
                ### con reverse recontruyo la URL
                guardaActuArch(tipoNombre, agencia + "-" + ano+ "-" + str(meses), "concilio", request)

                fsock = open(filePath, "rb")
                response = HttpResponse(fsock, content_type='application/force-download')
                ##print(filePath)
                ##print("ok aqui estoy")
                newFileName  = filePath.split("/" + agencia + '/')[1].strip()
                response['Content-Disposition'] = 'attachment; filename=' + newFileName
                status = "Conciliado"
                ##messages.success(request, "La conciliación se ejecuto correctamente!")
                return response
                ##return HttpResponseRedirect(reverse('reportesVC:conciliacionSAT', kwargs={'tipoNombre': tipoNombre, 'status': status}))
        elif ('bajaArchivo' == str(request.POST.getlist('boton')[0]) or 'subeArchivo' == str(request.POST.getlist('boton')[0])):
            return subirArchivoCon(request, tipoNombre, status)
        else:
            return HttpResponseRedirect(reverse('reportesVC:conciliacionSAT', kwargs={'tipoNombre': tipoNombre, 'status': status}))

@login_required
@permission_required('reportesVC.can_run_Conciliacion')
def conciliaIngresos(request, tipoNombre, status):
        if 'conciliar' == str(request.POST.getlist('boton')[0]):
            ##print("entre")
            variables = {}
            ##print(str(request.POST.getlist('CBAgencia')))
            agencia = str(request.POST.getlist('CBAgencia')[0])
            fecha = str(request.POST.getlist('DATEreportes')[0])
            meses = []
            if (fecha == ''):
                fecha = datetime.datetime.today().strftime('%Y-%m-%d')
                ano = datetime.datetime.today().strftime('%y')
                meses.append(int(datetime.datetime.today().strftime('%m')))
            else:
                ano = int(fecha[2:4])
                meses.append(int(fecha[5:7]))
            print("ano: " + str(ano))
            print("mes: " + str(meses))

            ###Ejecuto reporte
            dirConc = dirArchivos + tipoNombre + "/"
            conciIngresos = ConciliadorSAT(agencia, dirConc, meses,ano)

            ### Conciliacion SAT/ICAAV/Ingresos
            conciIngresos.extractInfoDiariosIngresos()
            conciIngresos.extractInfoVentas()

            if (len(conciIngresos.wriErr.mensajesErr) == 0):
                filePath = conciIngresos.recorreResDiariosVentas()
            if len(conciIngresos.wriErr.mensajesErr) > 0:
                print("entre aqui errores!!!")
                print(str(conciIngresos.wriErr.mensajesErr))
                getMessages(request, conciIngresos.wriErr.mensajesErr)
                return HttpResponseRedirect(
                    reverse('reportesVC:conciliacionIngresos', kwargs={'tipoNombre': tipoNombre, 'status': status}))

            else:
                ###Por último muestro resultado
                ### con HttpResponseRedirect evito que se de doble click y se vuelva a ejecutar
                ### con reverse recontruyo la URL
                guardaActuArch(tipoNombre, agencia + "-" + ano+ "-" + str(meses), "concilio", request)

                fsock = open(filePath, "rb")
                response = HttpResponse(fsock, content_type='application/force-download')
                ##print(filePath)
                ##print("ok aqui estoy")
                newFileName  = filePath.split("/" + agencia + '/')[1].strip()
                response['Content-Disposition'] = 'attachment; filename=' + newFileName
                status = "Conciliado"
                ##messages.success(request, "La conciliación se ejecuto correctamente!")
                return response
                ##return HttpResponseRedirect(reverse('reportesVC:conciliacionSAT', kwargs={'tipoNombre': tipoNombre, 'status': status}))
        elif ('bajaArchivo' == str(request.POST.getlist('boton')[0]) or 'subeArchivo' == str(request.POST.getlist('boton')[0])):
            return subirArchivoCon(request, tipoNombre, status)
        else:
            return HttpResponseRedirect(reverse('reportesVC:conciliacionIngresos', kwargs={'tipoNombre': tipoNombre, 'status': status}))
from django.conf.urls import url

from . import views

app_name = 'reportesVC'
urlpatterns = [
    ##(?P<question_id>[0-9]+)
    ###View normal
    #url(r'^(?P<tipoNombre>[\w]+)/(?P<reporteId>[0-9]+)/$', views.reporte, name='reporte'),
    ###Quick view provided bydjango
    url(r'^$', views.index, name='index'),

    ##url(r'^rp(?P<tipoNombre>[\w]+)/$', views.reportes, name='reportes'),
    url(r'^rp(?P<tipoNombre>[\w]+)/st(?P<status>[\w]+)/$', views.reportes, name='reportes'),
    url(r'^rp(?P<tipoNombre>[\w]+)/st(?P<status>[\w]+)/new/$', views.creaReporte, name='creaReporte'),
    url(r'^rp(?P<tipoNombre>[\w]+)/st(?P<status>[\w]+)/subirArchivo/$', views.subirArchivo, name='subirArchivo'),
    url(r'^rp(?P<tipoNombre>[\w]+)/(?P<pk>[0-9]+)/$', views.ReporteView.as_view(), name='reporte'),
    url(r'^rp(?P<tipoNombre>[\w]+)/(?P<pk>[0-9]+)/descargarZip/$', views.descargarZip, name='descargarZip'),
    url(r'^rp(?P<tipoNombre>[\w]+)/(?P<pk>[0-9]+)/descargarRepCXC/$', views.descargarRepCXC, name='descargarRepCXC'),

    url(r'^cal(?P<tipoNombre>[\w]+)/st(?P<status>[\w]+)/$', views.calculos, name='calculos'),
    url(r'^cal(?P<tipoNombre>[\w]+)/st(?P<status>[\w]+)/new/$', views.ejecutaComisiones, name='ejecutaComisiones'),
    url(r'^cal(?P<tipoNombre>[\w]+)/st(?P<status>[\w]+)/subirArchivo/$', views.subirArchivoCal, name='subirArchivoCal'),
    url(r'^cal(?P<tipoNombre>[\w]+)/(?P<pk>[0-9]+)/$', views.CalculoView.as_view(), name='calculo'),
    url(r'^cal(?P<tipoNombre>[\w]+)/(?P<pk>[0-9]+)/descargarFile/$', views.descargarFile, name='descargarFile'),

    url(r'^admin/Conta/$', views.adminConta, name='adminConta'),

    url(r'^con(?P<tipoNombre>[\w]+)/st(?P<status>[\w]+)/conciliacionBancos$', views.conciliacionBancos, name='conciliacionBancos'),
    url(r'^con(?P<tipoNombre>[\w]+)/st(?P<status>[\w]+)/conciliaBancos/$', views.conciliaBancos, name='conciliaBancos'),
    url(r'^con(?P<tipoNombre>[\w]+)/st(?P<status>[\w]+)/subirArchivoCon/$', views.subirArchivoCon, name='subirArchivoCon'),
    url(r'^con(?P<tipoNombre>[\w]+)/st(?P<status>[\w]+)/conciliacionSAT$', views.conciliacionSAT, name='conciliacionSAT'),
    url(r'^con(?P<tipoNombre>[\w]+)/st(?P<status>[\w]+)/conciliaSAT/$', views.conciliaSAT, name='conciliaSAT'),
    url(r'^con(?P<tipoNombre>[\w]+)/st(?P<status>[\w]+)/conciliacionIngresos$', views.conciliacionIngresos, name='conciliacionIngresos'),
    url(r'^con(?P<tipoNombre>[\w]+)/st(?P<status>[\w]+)/conciliaIngresos/$', views.conciliaIngresos, name='conciliaIngresos'),
    url(r'^con(?P<tipoNombre>[\w]+)/st(?P<status>[\w]+)/conciliacionMontoClave$', views.conciliacionMontoClave, name='conciliacionMontoClave'),
    url(r'^con(?P<tipoNombre>[\w]+)/st(?P<status>[\w]+)/conciliaMontoClave/$', views.conciliaMontoClave, name='conciliaMontoClave'),
]

from django.conf.urls import url

from . import views

app_name = 'reportesVC'
urlpatterns = [
    ##(?P<question_id>[0-9]+)
    ###View normal
    #url(r'^(?P<tipoNombre>[\w]+)/(?P<reporteId>[0-9]+)/$', views.reporte, name='reporte'),
    ###Quick view provided bydjango
    url(r'^$', views.index, name='index'),
    url(r'^rp(?P<tipoNombre>[\w]+)/(?P<pk>[0-9]+)/$', views.ReporteView.as_view(), name='reporte'),
    url(r'^rp(?P<tipoNombre>[\w]+)/(?P<pk>[0-9]+)/descargarZip/$', views.descargarZip, name='descargarZip'),
    ##url(r'^rp(?P<tipoNombre>[\w]+)/$', views.reportes, name='reportes'),
    url(r'^rp(?P<tipoNombre>[\w]+)/st(?P<status>[\w]+)/$', views.reportes, name='reportes'),
    url(r'^rp(?P<tipoNombre>[\w]+)/st(?P<status>[\w]+)/new/$', views.creaReporte, name='creaReporte'),
    url(r'^rp(?P<tipoNombre>[\w]+)/st(?P<status>[\w]+)/subirArchivo/$', views.subirArchivo, name='subirArchivo'),
    
]

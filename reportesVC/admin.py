from django.contrib import admin

# Register your models here.

from .models import EjecucionReporte, MesReporte, VariablesUltimoReporte, TipoReporte,ActualizacionesArchivos,Compania,CompaniaUsuario

admin.site.register(EjecucionReporte)
admin.site.register(MesReporte)
admin.site.register(VariablesUltimoReporte)
admin.site.register(TipoReporte)
admin.site.register(ActualizacionesArchivos)
admin.site.register(Compania)
admin.site.register(CompaniaUsuario)


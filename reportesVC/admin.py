from django.contrib import admin

# Register your models here.

from .models import EjecucionReporte, MesReporte, VariablesUltimoReporte, TipoReporte

admin.site.register(EjecucionReporte)
admin.site.register(MesReporte)
admin.site.register(VariablesUltimoReporte)
admin.site.register(TipoReporte)

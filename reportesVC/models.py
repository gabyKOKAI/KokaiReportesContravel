from django.db import models
from django.conf import settings

# Create your models here.

'''
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
'''
class TipoReporte(models.Model):
    def __str__(self):
        return str(self.id) + ": " + self.nombre + " - " + self.nombreLargo
    ##comisiones o ventas
    nombre = models.CharField(max_length=20)
    nombreLargo = models.CharField(max_length=20,default='')

class MesReporte(models.Model):
    def __str__(self):
        return str(self.id) + ": "  + self.nombre
    ##Enero, Febrero
    nombre = models.CharField(max_length=20)

class VariablesUltimoReporte(models.Model):
    def __str__(self):
        return str(self.id) + ": "  + self.nombre + "-" + self.valor
    nombre = models.CharField(max_length=20)
    valor =  models.CharField(max_length=50)
    editable = models.BooleanField()

class EjecucionReporte(models.Model):
    class Meta:
        permissions = (("can_run_Report", "Ejecuta Reporte"),("can_run_Calculos", "Ejecuta Calculos"),("can_run_Conciliacion", "Ejecuta Conciliacion"),("can_run_AdminConta", "Administracion Conta"))
    def __str__(self):
        return str(self.id) + ": "  + str(self.fechaEjecucion)
    tipoReporte = models.ForeignKey(TipoReporte, on_delete=models.CASCADE)
    mesPeriodo = models.ForeignKey(MesReporte, on_delete=models.CASCADE)
    semana = models.CharField(max_length=2)
    anoPeriodo = models.CharField(max_length=4)
    diaIniciaPeriodo = models.CharField(max_length=2)
    diaFinPeriodo = models.CharField(max_length=2)
    fechaEjecucion = models.DateTimeField('Fecha de ejecucion')
    estatus = models.CharField(max_length=10, default='')
    nombreArchivo = models.CharField(max_length=50,default='')
    rutaArchivo = models.CharField(max_length=100,default='')
    nombreZip = models.CharField(max_length=50,default='')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class ActualizacionesArchivos(models.Model):
    def __str__(self):
        return str(self.id) + ": "  + str(self.fechaEjecucion) + "-" + str(self.user) + "-" + self.tipoReporte.nombre + "-" + self.nombreArchivo
    tipoReporte = models.ForeignKey(TipoReporte, on_delete=models.CASCADE)
    nombreArchivo = models.CharField(max_length=50, default='')
    estatus=  models.CharField(max_length=10, default='')
    fechaEjecucion = models.DateTimeField('Fecha de ejecucion',auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1,on_delete=models.CASCADE)

class Compania(models.Model):
    def __str__(self):
        return str(self.id) + ": " + self.nombre
    nombre = models.CharField(max_length=255, blank=True)

class CompaniaUsuario(models.Model):
    def __str__(self):
        return str(self.id) + ": " + self.user.nombre + "-" + self.compania.nombre

    compania = models.ForeignKey(Compania, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
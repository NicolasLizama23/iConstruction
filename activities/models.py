from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre')
    description = models.TextField(blank=True, verbose_name='Descripción')
    start_date = models.DateField(null=True, blank=True, verbose_name='Fecha de Inicio')
    end_date = models.DateField(null=True, blank=True, verbose_name='Fecha de Fin')

    def __str__(self): return self.name

    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'

class Activity(models.Model):
    STATUS = [('pendiente','Pendiente'),('en_progreso','En progreso'),('completada','Completada')]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='activities', verbose_name='Proyecto')
    name = models.CharField(max_length=150, verbose_name='Nombre')
    planned_start = models.DateField(null=True, blank=True, verbose_name='Inicio Planificado')
    planned_end = models.DateField(null=True, blank=True, verbose_name='Fin Planificado')
    progress_percent = models.PositiveIntegerField(default=0, verbose_name='Progreso (%)')
    status = models.CharField(max_length=20, choices=STATUS, default='pendiente', verbose_name='Estado')

    def __str__(self): return f"{self.project} - {self.name}"

    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'

class ActivityLog(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='logs', verbose_name='Actividad')
    date = models.DateField(verbose_name='Fecha')
    progress_percent = models.PositiveIntegerField(verbose_name='Progreso (%)')
    notes = models.TextField(blank=True, verbose_name='Notas')

    def __str__(self): return f"{self.activity} {self.date} {self.progress_percent}%"

    class Meta:
        verbose_name = 'Registro de Actividad'
        verbose_name_plural = 'Registros de Actividades'

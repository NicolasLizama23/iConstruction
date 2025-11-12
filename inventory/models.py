from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Material(models.Model):
    UNIT_CHOICES = [
        ('un', 'Unidad'),
        ('kg', 'Kilogramo'),
        ('m', 'Metro'),
        ('lt', 'Litro'),
    ]
    name = models.CharField(max_length=120, verbose_name='Nombre')
    description = models.TextField(blank=True, verbose_name='Descripción')
    unit = models.CharField(max_length=4, choices=UNIT_CHOICES, default='un', verbose_name='Unidad')
    stock = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Stock')
    min_stock = models.DecimalField(max_digits=12, decimal_places=2, default=0, verbose_name='Stock Mínimo')

    def __str__(self): return self.name

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiales'

class Tool(models.Model):
    STATUS = [('disponible','Disponible'),('asignada','Asignada'),('mantenimiento','Mantenimiento')]
    code = models.CharField(max_length=50, unique=True, verbose_name='Código')
    name = models.CharField(max_length=120, verbose_name='Nombre')
    status = models.CharField(max_length=20, choices=STATUS, default='disponible', verbose_name='Estado')
    assigned_to = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='tools', verbose_name='Asignada a')
    notes = models.TextField(blank=True, verbose_name='Notas')

    def __str__(self): return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = 'Herramienta'
        verbose_name_plural = 'Herramientas'

class MaterialMovement(models.Model):
    KIND = [('ingreso','Ingreso'), ('salida','Salida')]
    material = models.ForeignKey(Material, on_delete=models.CASCADE, verbose_name='Material')
    kind = models.CharField(max_length=10, choices=KIND, verbose_name='Tipo')
    quantity = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Cantidad')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Usuario')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    notes = models.TextField(blank=True, verbose_name='Notas')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Movimiento de Material'
        verbose_name_plural = 'Movimientos de Materiales'

    def __str__(self): return f"{self.kind} {self.quantity} de {self.material}"

class ToolAssignment(models.Model):
    tool = models.ForeignKey(Tool, on_delete=models.CASCADE, verbose_name='Herramienta')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Usuario')
    assigned_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Asignación')
    returned_at = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de Devolución')
    notes = models.TextField(blank=True, verbose_name='Notas')

    def __str__(self): return f"{self.tool} -> {self.user}"

    class Meta:
        verbose_name = 'Asignación de Herramienta'
        verbose_name_plural = 'Asignaciones de Herramientas'

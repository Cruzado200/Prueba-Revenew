from django.db import models


class OptimizationJob(models.Model):
    """
    Representa una ejecución de optimización.
    Almacena el CSV subido, los parámetros de capacidad,
    y la solución resultante en formato JSON.
    """
    csv_file = models.FileField(
        upload_to='uploads/',
        help_text='Archivo CSV con datos de optimización'
    )
    cap_machine1 = models.FloatField(
        help_text='Capacidad disponible de la máquina 1 (horas)'
    )
    cap_machine2 = models.FloatField(
        help_text='Capacidad disponible de la máquina 2 (horas)'
    )
    result = models.JSONField(
        null=True,
        blank=True,
        help_text='Solución del modelo de optimización como JSON'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='Fecha y hora de la ejecución'
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Job de Optimización'
        verbose_name_plural = 'Jobs de Optimización'

    def __str__(self):
        return f"Job {self.id} - {self.created_at:%Y-%m-%d %H:%M}"

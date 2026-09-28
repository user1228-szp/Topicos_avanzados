from django.db import models

class cancion(models.Model):
    spotify_id = models.CharField(max_length=22, unique=True)
    titulo = models.CharField(max_length=300)
    artista = models.CharField(max_length=300)
    album = models.CharField(max_length=200, blank=True)
    genero = models.CharField(max_length=100)
    popularidad = models.PositiveSmallIntegerField()
    duracion_ms = models.PositiveIntegerField()
    
    fecha_lanzamiento = models.CharField(max_length=10, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-popularidad']
        verbose_name_plural = 'Canciones'
        
    def __str__(self):
        return f"{self.titulo} - {self.artista}"
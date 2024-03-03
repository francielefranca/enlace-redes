from django.db import models

# Create your models here.

class Enlace(models.Model):
    input_text = models.TextField()
    dest_mac = models.CharField(max_length=100)
    src_mac = models.CharField(max_length=100)
    encapsulated_frame = models.CharField(max_length=500)
    crc = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.input_text} (MAC - origem: {self.src_mac})'
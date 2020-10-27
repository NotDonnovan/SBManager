from django.db import models

class Seedbox(models.Model):
    name = models.CharField(max_length=20, default='')
    host = models.GenericIPAddressField()
    login = models.CharField(max_length=100, default='admin')
    password = models.CharField(max_length=100, default='')
    port = models.FloatField(default=8080)

    def __str__(self):
        return '{} ({})'.format(self.name, self.host)

    class Meta:
        verbose_name_plural = 'Seedboxes'

from django.db import models


class Seedbox(models.Model):
    name = models.CharField(max_length=20, default='')
    host = models.GenericIPAddressField()
    login = models.CharField(max_length=100, default='admin')
    password = models.CharField(max_length=100, default='')
    port = models.IntegerField(default=8080)
    save_loc = models.CharField(max_length=200, default='/')

    def __str__(self):
        return '{} ({})'.format(self.name, self.host)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


class Category(models.Model):
    name = models.CharField(max_length=20, default='')
    path = models.CharField(max_length=200, default='None', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Device(models.Model):
    name = models.CharField(max_length=20, default='')
    host = models.GenericIPAddressField(default='')

    def __str__(self):
        return self.name


class Directory(models.Model):
    device = models.ForeignKey('Device', related_name='location', on_delete=models.CASCADE)
    label = models.CharField(max_length=20, default='')
    path = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.device}/{self.label}'

    class Meta:
        verbose_name_plural = 'Directories'


class MoveQueue(models.Model):
    filename = models.CharField(max_length=200, default='')
    category = models.CharField(max_length=20, default='')

    def __str__(self):
        return self.filename

    class Meta:
        verbose_name = 'Queue'
        verbose_name_plural = 'Queue'

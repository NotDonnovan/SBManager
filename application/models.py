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
    device = models.ForeignKey('Device', related_name='category', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=20, default='')
    path = models.CharField(max_length=200, default='None', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Device(models.Model):
    name = models.CharField(max_length=20, default='')
    host = models.GenericIPAddressField(default='')
    type = models.CharField(max_length=20, default='Local')
    user = models.CharField(max_length=20, default='')
    password = models.CharField(max_length=100, default='')

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
    client = models.ForeignKey('Seedbox', related_name='queue', on_delete=models.CASCADE, blank=True, null=True)
    filename = models.CharField(max_length=200, default='')
    category = models.ForeignKey('Category', related_name='queue_cat', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.filename

    class Meta:
        verbose_name = 'Queue'
        verbose_name_plural = 'Queue'


class Moved(models.Model):
    filename = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.filename

    class Meta:
        verbose_name_plural = 'Moved'

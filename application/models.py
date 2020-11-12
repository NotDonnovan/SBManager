from django.db import models


class Seedbox(models.Model):
    name = models.CharField(max_length=20, default='')
    host = models.GenericIPAddressField()
    login = models.CharField(max_length=100, default='admin')
    password = models.CharField(max_length=100, default='')
    port = models.IntegerField(default=8080)
    save_loc = models.CharField(max_length=200, default='/')
    user = models.CharField(max_length=20, default='')

    def __str__(self):
        return '{} ({})'.format(self.name, self.host)

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


class Torrent(models.Model):
    client = models.ForeignKey('Seedbox', related_name='torrent_client', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', related_name='torrent_category', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default='N/A')
    state = models.CharField(max_length=50, default='')
    progress = models.IntegerField()
    size = models.CharField(max_length=10, default='')
    ratio = models.FloatField()

    def __str__(self):
        return self.name

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
    type = models.CharField(max_length=20, default='ssh')
    user = models.CharField(max_length=20, default='')

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
    torrent = models.ForeignKey('Torrent', related_name='queue', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, default='queued')

    def __str__(self):
        return self.torrent.name

    class Meta:
        verbose_name = 'Queue'
        verbose_name_plural = 'Queue'

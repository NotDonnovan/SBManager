import django_tables2 as tables
from .models import Seedbox, Torrent
from django_tables2.utils import A
from django.utils.html import format_html


class TorrentTable(tables.Table):

    class Meta:
        model = Torrent
        template_name = "application/table_template.html"
        sequence = ('client', 'name', 'category', 'state', 'ratio', 'size', 'progress')
        exclude = ('id', )
        attrs = {'class': 'highlight centered'}

    def render_client(self, record):
        return format_html(f'<a href="http://{record.client.host}:{record.client.port}">{record.client.name}</a>')

    def render_progress(self, record):
        return format_html(f'<div class="container">'
                           f'<label>{record.progress} %</label>'
                           f'<div class="progress">'
                           f'<div class="determinate" style="width: {record.progress}%"></div>'
                           f'</div>'
                           f'</div>')


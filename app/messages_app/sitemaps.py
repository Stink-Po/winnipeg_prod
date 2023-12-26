from django.contrib.sitemaps import Sitemap
from .models import Message


class MessageSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Message.objects.all()

    def lastmod(self, obj):
        return obj.updated
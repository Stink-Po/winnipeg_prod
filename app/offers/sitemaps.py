from django.contrib.sitemaps import Sitemap
from .models import SiteOffers


class OffersSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return SiteOffers.objects.filter(
            availability=SiteOffers.Status.AVAILABLE
        ).order_by('-created_at')

    def lastmod(self, obj):
        return obj.created_at

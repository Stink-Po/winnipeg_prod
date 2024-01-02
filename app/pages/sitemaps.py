from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class PagesSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8
    protocol = 'https'

    def items(self):
        return [
            'pages:index',
            "pages:duct_cleaning",
            "pages:services",
            "pages:about",
            "pages:furnace_installation",
            "pages:furnace_repair",
            "pages:air_conditioner_tune_up",
            "pages:furnace_cleaning",
            "pages:air_conditioner_installation",
        ]

    def location(self, item):
        return reverse(item)

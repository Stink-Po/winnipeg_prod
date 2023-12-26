from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap
from pages.sitemaps import PagesSitemap
from offers.sitemaps import OffersSitemap

sitemaps = {
    'posts': PostSitemap,
    "pages": PagesSitemap,
    "offers": OffersSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("pages.urls")),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("blog/", include("blog.urls")),
    path("messages/", include("messages_app.urls")),
    path("order/", include("services.urls")),
    path("score/", include("score.urls")),
    path("mail_service/", include("mail_service.urls")),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
    path("projects/", include("projects.urls")),
    path("offers/", include("offers.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
handler404 = "pages.views.handler404_view"
handler500 = "pages.views.handler500_view"

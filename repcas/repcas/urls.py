from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('main.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/', include('accounts.urls')),
    # path('businesses/', include('businesses.urls')),
    # path('inventory/', include('inventory.urls')),
    # path('sales/', include('sales.urls')),
    # path('blog/', include('blog.urls')),
    # path('movements/', include('movements.urls')),
    # path('petty-cash/', include('petty_cash.urls')),
    # path('stats/', include('stats.urls')),
    path('admin/', admin.site.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

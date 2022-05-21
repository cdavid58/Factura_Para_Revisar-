from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include('home.urls')),
    url(r'^api/', include('api.urls')),
    url(r'^list_data/', include('list_data.urls')),
    url(r'^invoice/', include('invoice.urls')),
    url(r'^pos/', include('pos.urls')),
    url(r'^empleoyee/', include('empleoyee.urls')),
    url(r'^reports/', include('reports.urls')),
    url(r'^inventory/', include('inventory.urls')),
    url(r'^wallet/', include('wallet.urls')),
    url(r'^client/', include('client.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
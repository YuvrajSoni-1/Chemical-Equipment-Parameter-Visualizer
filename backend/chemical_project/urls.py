from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('', RedirectView.as_view(url='/api/', permanent=False)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

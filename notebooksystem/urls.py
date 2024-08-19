from django.contrib import admin
from django.urls import path, include
from utilisateurs.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('utilisateurs.urls')),
    path('cours/', include('cours.urls')),
    path('eleves/', include('eleves.urls')),
    path('notes/', include('notes.urls')),
    path('absences/', include('absences.urls')),
    path('rapports/', include('rapports.urls')),
    path('notifications/', include('notifications.urls')),
    path('api/', include('tableau_de_bord.urls')),
    path('parametres/', include('parametres.urls')),
    path('licences/', include('licences.urls')),
    path('classes/', include('classes.urls')),
]

urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
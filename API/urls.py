from django.urls import path, include

from .views import upload_video_view


urlpatterns = [
    
    path('users/', include('users.urls')),
    path('accueil/', include('accueil.urls')),
    path('demande/', include('demande.urls')),
    path('evenement/', include('evenement.urls')),
    path('abonnement/', include('abonnement.urls')),
    path('profil/', include('profil.urls')),

    path("videos/upload/", upload_video_view, name="upload_video"),

    path('activities/', include('activities.urls')),
    path('badges/', include('badges.urls')),

]

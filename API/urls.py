from django.urls import path, include
from demande.views import DemandeViewSet
from rest_framework.routers import DefaultRouter

# Créer un router pour les demandes avec l'URL correcte
demande_router = DefaultRouter()
demande_router.register(r'', DemandeViewSet, basename='demande')

urlpatterns = [
    
    path('users/', include('users.urls')),
    path('accueil/', include('accueil.urls')),
    path('demandes/', include(demande_router.urls)),
    path('evenement/', include('evenement.urls')),
    path('abonnement/', include('abonnement.urls')),
    path('profil/', include('profil.urls')),

    path('activities/', include('activities.urls')),
    path('badges/', include('badges.urls')),

]

from django.urls import path, include


urlpatterns = [
    
    path('users/', include('users.urls')),
    path('accueil/', include('accueil.urls')),
    path('demande/', include('demande.urls')),
    path('evenement/', include('evenement.urls')),
    path('abonnement/', include('abonnement.urls')),
    path('profil/', include('profil.urls')),

    path('activities/', include('activities.urls')),
    path('badges/', include('badges.urls')),

]

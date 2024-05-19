from django.urls import path

from . import views

app_name = "builder-video"
urlpatterns = [
    path("", view=views.index, name="index"),
    path("netflix/", view=views.NetflixView.as_view(), name="netflix"),
    path("netflix/boxoffice/", view=views.index, name="netflix-boxoffice"),
    
]

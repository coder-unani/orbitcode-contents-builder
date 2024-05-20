from django.urls import path

from . import views

app_name = "builder-video"
urlpatterns = [
    path("", view=views.index, name="index"),
    path("netflix/", view=views.NetflixFindView.as_view(), name="netflix"),
    # path("netflix/<int:pk>/", view=views.NetflixDetailView.as_view(), name="netflix-detail")
    path("netflix/boxoffice/", view=views.NetflixBoxOfficeView.as_view(), name="netflix-boxoffice"),
]

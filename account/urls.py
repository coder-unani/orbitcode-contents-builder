from django.urls import path

from . import views

app_name = "account"
urlpatterns = [
    path("", view=views.index, name="index"),
]
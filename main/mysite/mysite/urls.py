from django.contrib import admin
from django.urls import include, path

from userstest import views

urlpatterns = [
    path("polls/", include("polls.urls")),
    path("admin/", admin.site.urls),
    path("api/users/check_user", views.check_user, name="check_user"),
]
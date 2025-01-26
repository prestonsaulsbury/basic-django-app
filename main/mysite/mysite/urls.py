from django.contrib import admin
from django.urls import include, path

from userstest import views

urlpatterns = [
    path("polls/", include("polls.urls")),
    path("admin/", admin.site.urls),
    path("api/users/check_user", views.check_user, name="check_user"),
    path("api/todos", views.todo_items, name="todo_item"),
    # path("api/todos/:id", views.add_todo_item, name="add_todo_item"),
    path('api/users/signup', views.sign_up, name='sign_up'),
    # path('', include('userstest.urls')),
]
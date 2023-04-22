from account import views
from django.urls import path

app_name = "account"

urlpatterns = [
    path("login/", views.login_view_func, name="login"), 
    path("login_func/", views.login_view, name="login_func"), 
    path("register/" , views.register_view, name="register"),
    path("logout/", views.logout_view, name='logout-view'),
]
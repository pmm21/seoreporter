from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.signupView),
    path('customer/', views.CustomerView)
]

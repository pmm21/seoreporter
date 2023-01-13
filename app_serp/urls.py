from django.urls import path
from . import views

urlpatterns = [
    path('get-location-code/', views.LocationCodeView.as_view()),
    path('project-list/', views.ProjectListView.as_view()),
    path('project/', views.ProjectView.as_view()),
    path('project-add/', views.ProjectAddView.as_view()),
    path('dashboard/', views.DashboardView.as_view()),
    path('topic/', views.TopicView.as_view())
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/todos/', views.todos),
    path('api/todos/<todo_id>/', views.todo_detail),  
]
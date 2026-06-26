from django.urls import path
from . import views

urlpatterns = [
    path('', views.mashina_list, name='mashina_list'),
    path('create/', views.mashina_create, name='mashina_create'),
    path('update/<int:id>/', views.mashina_update, name='mashina_update'),
    path('delete/<int:id>/', views.mashina_delete, name='mashina_delete'),

    path('api/chat/', views.chat_response, name='chat_response'),
]
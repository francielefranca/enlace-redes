from django.urls import path
from . import views

app_name = 'enlaceapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('sobre/', views.sobre, name='sobre'),
    path('contato/', views.contato, name='contato'),
    path('simulador_enlace/', views.simulador_enlace, name='simulador_enlace'),
    path('resultado_simulador/', views.resultado_simulador, name='resultado_simulador'),
    path('ospf/', views.ospf, name='ospf'),
    path('resultado_ospf/', views.resultado_ospf, name='resultado_ospf'),

]
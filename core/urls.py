from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='home'),
    path('amortizacion/', views.amortization_view, name='amortization'),
    path('fondo-amortizacion/', views.sinking_fund_view, name='sinking_fund'),
    path('mis-tablas/', views.my_tables, name='my_tables'),
    path('mis-fondos/', views.my_funds, name='my_funds'),
    path('guardar-amortizacion/', views.save_amortization, name='save_amortization'),
    path('guardar-fondo/', views.save_fund, name='save_fund'),
    path('tabla/<int:id>/', views.table_detail, name='table_detail'),
    path('fondo/<int:id>/', views.fund_detail, name='fund_detail'),
    path('registro/', views.signup, name='signup'),
    path('confirmacion-salida/', TemplateView.as_view(template_name='confirmation.html'), name='logout_confirmation'),
    path('recursos-educativos/', views.recursos_educativos, name='recursos_educativos'),
    path('acerca-de/', views.acerca_de, name='acerca_de'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('amortizacion/', views.amortization_view, name='amortization'),
    path('fondo-amortizacion/', views.sinking_fund_view, name='sinking_fund'),
]

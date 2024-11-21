from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('amortization/', views.amortization_view, name='amortization'),
    path('sinking_fund/', views.sinking_fund_view, name='sinking_fund'),
    path('my_tables/', views.my_tables, name='my_tables'),
    path('my_funds/', views.my_funds, name='my_funds'),
    path('save_amortization/', views.save_amortization, name='save_amortization'),
    path('save_fund/', views.save_fund, name='save_fund'),
    path('table/<int:id>/', views.table_detail, name='table_detail'),
    path('fund/<int:id>/', views.fund_detail, name='fund_detail'),
    path('signup/', views.signup, name='signup'),
]

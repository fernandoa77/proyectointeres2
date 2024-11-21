from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('cuentas/iniciar-sesion/', auth_views.LoginView.as_view(), name='login'),
    path('cuentas/cerrar-sesion/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('cuentas/', include('django.contrib.auth.urls')),
]

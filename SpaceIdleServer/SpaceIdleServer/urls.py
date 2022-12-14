"""
SpaceIdleServer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/

Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Uncomment next two lines to enable admin:
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    # Uncomment the next line to enable the admin:
    path('admin/', admin.site.urls),
    path('activity_log/', views.activity_log, name='activity_log'),
    path('enter_code/', views.enter_code, name='enter_code'),
    path('cloud_save/', views.cloud_save, name='cloud_save'),
    path('get_cloud_save/', views.get_cloud_save, name='get_cloud_save'),
    path('cloud_register/', views.cloud_register, name='cloud_register'),
    path('cloud_login/', views.cloud_login, name='cloud_login'),
    path('progress_graph/', views.progress_graph, name='progress_graph'),
    path('abandon_graph/', views.abandon_graph, name='abandon_graph'),
    path('sector_graph/', views.sector_graph, name='sector_graph'),
]

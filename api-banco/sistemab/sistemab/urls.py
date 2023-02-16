"""sistemab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from saveresults import viewsets as sareresultsviewsets

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from saveresults.viewsets import LogoutView

route = routers.DefaultRouter()


route.register(r'api/monitoring', sareresultsviewsets.Detection,
               basename='detection')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/autentication/login',
         TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/autentication/renovate',
         TokenRefreshView.as_view(), name='token_refresh'),
    path('api/autentication/logout', LogoutView.as_view(), name='auth_logout'),
    path('', include(route.urls))
]

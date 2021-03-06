"""exeldb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from table import views as tw

urlpatterns = [
    path('admin/', admin.site.urls),    
    path('search/', tw.db_search),
    path('show/<id>', tw.db_show),
    path('upload/', tw.upload),
    path('changeCell/', tw.changeCell),    
    path('download/<id>', tw.download),
    path('delete/<id>', tw.delete),
    path('changeName/', tw.changeName),
    path('login/', tw.login),
    path('', tw.index),
]

"""mobile_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from mobile_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.shop_log),
    path('logout',views.shop_logout),
    path('register',views.user_reg),
    path('shop_home',views.shop_home),
    path('user_home',views.user_home),
    path('category',views.category),
    path('add_pro',views.add_pro),
    path('details',views.details),
    path('delete/<pid>',views.delete),
    path('edit_pro/<pid>',views.edit_pro),
    path('edit_details/<pid>',views.edit_details,name="edit_details"),
    path('delete_details/<pid>',views.delete_details),
    path('user_view/<pid>',views.user_view),
    path('add_cart/<cid>',views.add_cart),
    
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
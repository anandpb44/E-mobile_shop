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
    path('',views.home),
    path('login',views.shop_log),
    path('logout',views.shop_logout),
    path('register',views.user_reg),
    path('validate/<name>/<password>/<email>/<otp>',views.validate,name="validate"),
    path('shop_home',views.shop_home),
    path('user_home',views.user_home),
    path('brand/<int:brand_id>/', views.brand_products, name='brand_products'),
    path('category',views.category),
    path('add_pro',views.add_pro),
    path('view/<pid>',views.admin_view),
    path('details',views.details),
    path('delete/<pid>',views.delete),
    path('edit_pro/<pid>',views.edit_pro),
    path('edit_details/<pid>',views.edit_details,name="edit_details"),
    path('delete_details/<pid>',views.delete_details),
    path('admin_booking',views.ad_booking),

    path('user_view/<int:pid>',views.user_view,name="user_view"),
    path('add_cart/<cid>',views.add_cart),
    path('view_cart',views.view_cart),
    path('delete_cart/<pid>',views.deleteCart),
    path('qty_incr/<cid>',views.qty_incr),
    path('qty_decr/<cid>',views.qty_decr),
    path('buy_now/<pid>',views.buy_now),
    path('cart_buy',views.cart_buy),
    path('user_booking',views.user_bookings),
    path('deletebookings/<pid>',views.delete_bookings),
    path('address',views.add_address),
    path('place_order/<detail>/<data>/<qty>/<price>',views.place_order,name="place_order"),
    path('payment/<pid>',views.order_payment,name="order_payment"),
    path('delete_address/<pid>',views.delete_address),
    path('bookings',views.bookings),
    path('bookings2',views.bookings2),
    path('place_order2/<qty>/<tprice>/<total>',views.place_order2,name="place_order2"),
    path('payment2',views.order_payment2,name="order_payment2"),
    path('callback',views.callback),
    path('callback2',views.callback2),

]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
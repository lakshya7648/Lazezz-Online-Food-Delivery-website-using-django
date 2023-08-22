"""
URL configuration for lazezz project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
import alpha.views as v
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', v.set_location,name="set_location"),
    path('index', v.set_location, name='set_location'),
    path('city', v.city_location,name="city_choice"),
    path('signup', v.sign_up,name="sign_up"),
    path('edit', v.edit_page,name="edit_page"),
    path('logout', v.logout_view,name="logout page"),
    # path('edit/<int:uid>',v.editdata,name="edit page"),
    # path('select_rest/<str:uid>', v.rest_view,name="restaurant page"),
    path('city2', v.verified,name="secure_page_loc2"),
    path('food_sel', v.food_select, name='Secure Food Select'),
    path('rest_sel', v.rest_done, name='Secure restaurant selected'),
    path('profile', v.my_profile, name='Secure profile page'),
    # path('cart', v.addcart, name='CARt'),
    path('cart', v.my_cart, name='CART'),
    # path('checkout', v.final_checkout, name='Secure Check Out')
    path('checkout', v.checkout,name='Secure Check Out'),
    path('confirm', v.confirmed,name='confirm Out'),
    # Restaurant Admin urls
    path('addrest', v.addRestaurant, name='Add Restaurant'),
    path('partner', v.partnerwithus, name='Partner With Us'),
    path('rest_registration', v.register_restaurant, name='Restaurant Registration'),
    path('login_rest', v.login_into_restaurant, name='Login Into Restaurant'),
    path('rlogout', v.logout_from_restaurant, name='Logout from dashboard'),
    path('update', v.update_food_item, name='food updation'),
    path('delete', v.delete_food_item, name = 'Food Deletion'),
    path('add', v.add_food_item, name='Add Food Item'),
    path('accept', v.accept_request, name='Accept Request'),
    path('accept_orders_online', v.accept_orders_online, name='Accept Orders online'),
    path('updateprofile', v.update_profile, name='Update Your Profile'),
    # Lazezz siteadmin urls
    path('a_login',v.loginPage,name="Login"),
    path('asignup',v.lazezz_admin_signup,name="Signup"), # m
    path('request',v.requests,name="Request"),
    path('error',v.error,name="Error"),
    path("alogout",v.lazezz_admin_logout_view, name='logout'), # m
    path("aedit/<int:sid>",v.editdata,name="Edit data"), # m
    path("verified",v.averified,name='verify'),
    path("unverified",v.unverified,name='unverify'),
    path("getNewOrders", v.getNewOrders, name="Get New Order"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

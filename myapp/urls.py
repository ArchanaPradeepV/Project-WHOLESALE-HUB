
from django.contrib import admin
from django.urls import path, include

from myapp import views

urlpatterns = [
    path('',views.landing_page),
    path("login",views.login),
    path('login_post',views.login_post),
    path("register",views.register),
    path('admin_home',views.admin_home),
    path('admin_manage_staff',views.admin_manage_staff),
    path('add_staff',views.add_staff),
    path('add_staff_post',views.add_staff_post),
    path('edit_staff/<id>',views.edit_staff),
    path('edtcat/<id>',views.edtcat),
    path('dltcat/<id>',views.dltcat),
    path('edit_staff_post',views.edit_staff_post),
    path('about',views.about),
    path('contact',views.contact),
    path('manage_category',views.manage_category),
    path('add_category',views.add_category),
    path('addcat',views.addcat),
    path('updtcat',views.updtcat,name='updtcat'),
    path('forgot_password',views.forgot_password),
    path('forgot_password_post',views.forgot_password_post),
    path('popup',views.popup),
    path('staff_home',views.staff_home),
    path('user_reg',views.user_reg),
    path('retailer_home',views.retailer_home),
    path('verify',views.verify),
    path('sretailers',views.sretailers),
    path('acceptretailer/<id>',views.acceptretailer),
    path('rejectretailer/<id>',views.rejectretailer),
    path('viewretailers',views.viewretailers),





]

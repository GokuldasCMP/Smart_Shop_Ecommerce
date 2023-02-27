from django.urls import path
from accounts import views


urlpatterns = [

    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('mobile-login/', views.mobile_login, name='mobile_login'),
    path('verify-codelogin/', views.verify_codelogin, name='verify_codelogin'),
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('order-detail/<int:order_id>/', views.order_detail, name='order_detail'),
    path('myAddress/', views.myAddress, name='myAddress'),
    path('addAddress/', views.addAddress, name='addAddress'),
    path('deleteAddress/<int:id>/', views.deleteAddress, name='deleteAddress'),
    path('editAddress/<int:id>/', views.editAddress, name='editAddress'),
    path('deleteCheckoutAddress/<int:id>/', views.deleteCheckoutAddress, name='deleteCheckoutAddress'),
    path('AddCheckoutAddress/', views.AddCheckoutAddress, name='AddCheckoutAddress'),
   
]

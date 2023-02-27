
from django.urls import path
from product import views

urlpatterns = [
    path('user-products/', views.user_products, name='user_products'),
    path('category/<slug:sub_category_slug>/', views.user_products, name='products_by_sub_category'),
    path('category/product/<int:product_id>/', views.product_details, name='product_details'),
    path('search/',views.search,name='search')     







]

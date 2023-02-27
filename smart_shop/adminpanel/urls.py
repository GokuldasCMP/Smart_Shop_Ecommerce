from django.urls import path
from .import views 


urlpatterns = [

    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('admin-dashbord/', views.dashbord, name='admin_dashbord'),
    path('admin-category/', views.admin_category, name='admin_category'),
    path('add-category/', views.add_category, name='add_category'),
    path('<int:id>/delete-category/',views.delete_category, name='delete_category'),
    path('<int:id>/update-category/', views.update_category, name='update_category'),
    path('admin-subcategory/', views.admin_subcategory, name='admin_subcategory'),
    path('add-subcategory/',views.add_subcategory, name='add_subcategory'),
    path('<int:id>/delete-subcategory/', views.delete_subcategory, name='delete_subcategory'),
    path('<int:id>/update-subcategory/', views.update_subcategory, name='update_subcategory'),
    path('admin-products/', views.admin_products, name='admin_products'),
    path('admin-addproducts/', views.admin_addproducts,name='admin_addproducts'),
    path('<int:id>/update-products/', views.update_products,name='update_products'),
    path('<int:id>/delete-products/', views.delete_products,name='delete_products'),
    path('users/', views.users, name='users'),
    path('adminlogout/', views.adminlogout, name='adminlogout'),
    path('<int:id>/blockuser/', views.blockuser, name='blockuser'),
    path('admin-orders/', views.admin_orders, name='admin_orders'),
    path('update-order/<int:id>',views.update_order,name="update_order"),
    path('coupon/', views.coupon,name='coupon'),    
    path('addCoupon/', views.addCoupon,name='addCoupon'),
    path('<int:id>/deleteCoupon/', views.deleteCoupon,name='deleteCoupon'),
    path('<int:id>/updateCoupon/', views.updateCoupon,name='updateCoupon'),
    path('variation/', views.variation,name='variation'), 
    path('<int:id>/delete_variation/', views.delete_variation,name='delete_variation'),
    path('<int:id>/update_variation/', views.update_variation,name='update_variation'),
    path('add_variation/', views.add_variation,name='add_variation'),
    path('salesReport/', views.salesReport,name='salesReport'),
    path('salesReportMonth/<int:id>',views.salesReportMonth,name="salesReportMonth"),
    path("salesReportYear/<int:id>",views.salesReportYear,name='salesReportYear'),
    path('pdfReport/<str:start_date>//<str:end_date>/', views.pdfReport, name='pdfReport'),
    path('excelReport/<str:start_date>//<str:end_date>/', views.excelReport, name='excelReport')
   
   

]

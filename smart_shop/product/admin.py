from django.contrib import admin
from .models import Product,Variations
# Register your models here.

class  ProductAdmin(admin.ModelAdmin):
    list_display=('product_name','price','stock','category','sub_category','is_available')
    prepopulated_fields= {'slug':('product_name',)}




class VariationsAdmin(admin.ModelAdmin):
    list_display=('product','variation_category','variation_value','stock','is_active','created_date',)
    list_editable=('is_active',)
    list_filter=('product','variation_category','variation_value',)

admin.site.register(Product,ProductAdmin)
admin.site.register(Variations,VariationsAdmin)
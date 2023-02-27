from product.models import Product,Variations
from django import forms
from .models import AdminLogin
from category.models import Category, Sub_Category
from orders.models import Coupon


class AdminLoginForm(forms.ModelForm):

    class Meta:
        model = AdminLogin
        fields = '__all__'
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter your password'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'})

        }

        labels = {
            'email': 'email',
            'password': 'password',
        }


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['category_name','slug']
        labels = {
            'category_name': 'category name',
                     'slug':'slug',

        }


class Update_categoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name','slug']
        labels = {
            'category_name': 'category name',
                     'slug':'slug'

        }


class Update_subcategoryForm(forms.ModelForm):
    class Meta:
        model = Sub_Category
        fields = ['sub_category_name','slug', 'category']
        labels = {
            'sub_category_name': 'sub_category_name',
                         'slug':'slug',
                     'category': 'category',
            
        }


class Sub_CategoryForm(forms.ModelForm):
    class Meta:
        model = Sub_Category
        fields = ['sub_category_name','slug', 'category',]
        labels = {
            'sub_category_name': ' sub_category_name',
                         'slug':'slug',
                     'category': 'category',
            

        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name','slug' ,'price', 'image','image1','image2','image3', 'stock', 'category','sub_category',]
        labels = {
            'product_name': 'product_name',
                   'slug' :'slug' ,
                   
                   'price': 'price',
                   'image': 'image',
                  'image1':'image1',
                  'image2':'image2',
                  'image3':'image3',
                   'stock': 'stock',
                'category': 'category',
            'sub_category':'sub_category'
           

        }


class Update_ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name','slug', 'price', 'image','image1','image2','image3', 'stock', 'category','sub_category',]
        labels = {
            'product_name': 'product_name',
                   'slug' :'slug' ,
                   'price': 'price',
                   'image': 'image',
                  'image1':'image1',
                  'image2':'image2',
                  'image3':'image3',
                   'stock': 'stock',
                'category': 'category',
            'sub_category':'sub_category'
           
        }



class DateInput(forms.DateInput):
    input_type = 'date'

class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'discount','min_value','valid_at','active']
        widgets = {
                    'valid_at': DateInput(),
                    }
        labels ={
            'code':'Coupon Code',
            'discount':'Discount',
            'min_value':'Minimum Value',
            'valid_at':'Expiry Date',
            'active':'Available',
            
        } 

class VariationForm(forms.ModelForm):
    class Meta:
        model = Variations
        fields = ['product','variation_category','variation_value','stock','is_active'] 
        labels ={
            'product':'product',
            'variation_category':'variation category',
            'variation_value':'variation value',
            'stock':'stock',
            'is_active':'is active',
            
        }

class Update_VariationForm(forms.ModelForm):
    class Meta:
        model = Variations
        fields = ['product','variation_category','variation_value','stock','is_active'] 
        labels ={
            'product':'product',
            'variation_category':'variation category',
            'variation_value':'variation value',
            'stock':'stock',
            'is_active':'is active',
            
        }





from django.db import models
from category.models import Sub_Category, Category
from PIL import Image

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)
    price = models.FloatField()
    image = models.ImageField(upload_to='products')
    image1 = models.ImageField(upload_to='products')
    image2 = models.ImageField(upload_to='products')
    image3 = models.ImageField(upload_to='products')
    stock = models.IntegerField()
    is_available=models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(Sub_Category,on_delete=models.CASCADE)
   
    def __str__(self):
        return self.product_name
    

class VariationManager(models.Manager):
        def colors(self):
             return super(VariationManager,self).filter(variation_category='color',is_active=True)
        
        def sizes(self):
             return super(VariationManager,self).filter(variation_category='size',is_active=True)
             
    
variation_category_choice=(

    ('color','color'),
    ('size','size')
)


class Variations(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    variation_category=models.CharField(max_length=100,choices=variation_category_choice)
    variation_value=models.CharField(max_length=100)
    stock = models.IntegerField(default=0)
    is_active=models.BooleanField(default=True)
    created_date=models.DateTimeField(auto_now=True)
     

    objects=VariationManager()

    def __str__(self):
        return self.variation_value
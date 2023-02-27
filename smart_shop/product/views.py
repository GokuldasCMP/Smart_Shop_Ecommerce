from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from category.models import Sub_Category, Category
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from my_cart.views import _cart_id
from my_cart.models import CartItem


def user_products(request, sub_category_slug=None):
    sub_category = None
    categories = None
    products = None

    if sub_category_slug != None:
        sub_category = get_object_or_404(Sub_Category, slug=sub_category_slug)
        products = Product.objects.filter(sub_category=sub_category, is_available=True).order_by('-id')
        categories = Category.objects.all()
        sub = Sub_Category.objects.all()
        product_count = products.count()
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
    else:

        categories = Category.objects.all()
        sub = Sub_Category.objects.all()
        products = Product.objects.all().order_by('-id')
        product_count = products.count()
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

    context = {
        'products': paged_products,
        'categories': categories,
        'sub': sub,
        'product_count': product_count
    }
    return render(request, 'products/user_products.html', context)


def product_details(request, product_id):
   try:
      single_product = Product.objects.get(id=product_id)
      in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
   except Exception as e:
        raise e
   context = {
       'single_product': single_product,
       'in_cart': in_cart,
               }
   return render(request, 'products/userside_product_details.html', context)


def search(request):
   categories = Category.objects.all()
   sub = Sub_Category.objects.all()
   products = None
   if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('is_available').filter(product_name__icontains=keyword)
            product_count = products.count()
        else:
           return redirect('user_products')    
   context = {

        'products': products,
        'categories':categories,
          'sub':sub,
        'product_count': product_count,
    }
   return render(request, 'products/user_products.html', context)

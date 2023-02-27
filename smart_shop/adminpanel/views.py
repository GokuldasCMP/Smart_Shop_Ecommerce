from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from .forms import AdminLoginForm
from accounts.models import CustomUser
from product.models import Product,Variations
from django.contrib import messages
from category.models import Category, Sub_Category
from orders.models import Order,Payment
from django.core.paginator import  Paginator
from .forms import Update_categoryForm, CategoryForm, Update_subcategoryForm, Sub_CategoryForm, ProductForm, Update_ProductForm,CouponForm,VariationForm,Update_VariationForm
from orders.models import Coupon
from datetime import datetime,timedelta,date
from django.db.models.functions import Cast
from django.http import HttpResponse
from django.template.loader import get_template
from django.db.models import Sum, Q, FloatField
from xhtml2pdf import pisa
import xlwt
# Create your views here.


def adminlogin(request):
    if 's_email' in request.session:
        return redirect('admin_dashbord')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None and user.is_superuser:

            request.session['s_email'] = email
            auth.login(request, user)
            print('admin logged in')
            messages.success(request, 'Successfully signed up!')
            return redirect('admin_dashbord')
        else:
            print('Not authorized')
            messages.error(request, 'Not autherised')
            return redirect('adminlogin')

    else:
        form = AdminLoginForm()
        dict_forms = {
            'form': form
        }

        return render(request, 'adminpanel/adminlogin.html', dict_forms)


#dashbord
def dashbord(request):
    today = datetime.today()
    today_date = today.strftime("%Y-%m-%d")
    month = today.month
    year = today.strftime("%Y")
    one_week = datetime.today() - timedelta(days=7)
    order_count_in_month = Order.objects.filter(created_at__year = year,created_at__month=month, is_ordered=True).count() 
    order_count_in_day =Order.objects.filter(created_at__date = today, is_ordered=True).count()
    order_count_in_week = Order.objects.filter(created_at__gte = one_week, is_ordered=True).count()
    number_of_users  = CustomUser.objects.filter(is_superuser = False).count()
    paypal_orders = Payment.objects.filter(payment_method="Paypal",status = 'True').count()
    cash_on_delivery_count = Payment.objects.filter(payment_method="Cash on Delivery",status = 'True').count()
    total_payment_count = paypal_orders  + cash_on_delivery_count
    try:
        total_payment_amount = Payment.objects.filter(status = 'True').annotate(total_amount=Cast('amount_paid', FloatField())).aggregate(Sum('total_amount'))
        
    except:
        total_payment_amount=0
        
    if total_payment_amount['total_amount__sum'] :
      revenue = total_payment_amount['total_amount__sum']
      revenue = format(revenue, '.2f')
    
    else:
      revenue = 0
           
    blocked_user = CustomUser.objects.filter(is_active = False,is_superuser = False).count()
    unblocked_user = CustomUser.objects.filter(is_active = True,is_superuser = False).count()

    today_sale = Order.objects.filter(created_at__date = today_date,payment__status = 'True', is_ordered=True).count()
    today = today.strftime("%A")
    new_date = datetime.today() - timedelta(days = 1)
    yester_day_sale =   Order.objects.filter(created_at__date = new_date,payment__status = 'True', is_ordered=True).count()  
    yesterday = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_2 = Order.objects.filter(created_at__date = new_date,payment__status = 'True', is_ordered=True).count()
    day_2_name = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_3 = Order.objects.filter(created_at__date = new_date,payment__status = 'True', is_ordered=True).count()
    day_3_name = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_4 = Order.objects.filter(created_at__date = new_date,payment__status = 'True', is_ordered=True).count()
    day_4_name = new_date.strftime("%A")
    new_date = new_date - timedelta(days = 1)
    day_5 = Order.objects.filter(created_at__date = new_date,payment__status = 'True', is_ordered=True).count()
    day_5_name = new_date.strftime("%A")
    # #status
    ordered = Order.objects.filter(status = 'Order Confirmed', is_ordered=True).count()
    shipped = Order.objects.filter(status = "Shipped").count()
    out_of_delivery = Order.objects.filter(status ="Out for delivery").count()
    delivered = Order.objects.filter(status = "Delivered").count()
    returned = Order.objects.filter(status = "Returned").count()
    cancelled = Order.objects.filter(status = "Cancelled").count()

    context ={
        'order_count_in_month':order_count_in_month,
        'order_count_in_day':order_count_in_day,
        'order_count_in_week':order_count_in_week,
        'number_of_users':number_of_users,
        'paypal_orders':paypal_orders,
        'total_payment_count':total_payment_count,
        'revenue':revenue,
        'ordered':ordered,
        'shipped':shipped,
        'out_of_delivery':out_of_delivery,
        'delivered':delivered,
        'returned':returned,
        'cancelled':cancelled,
        'cash_on_delivery_count':cash_on_delivery_count,
        'blocked_user':blocked_user,
        'unblocked_user':unblocked_user,
        'today_sale':today_sale,
        'yester_day_sale':yester_day_sale,
        'day_2':day_2,
        'day_3':day_3,
        'day_4':day_4,
        'day_5':day_5,
        'today':today,
        'yesterday':yesterday,
        'day_2_name':day_2_name,
        'day_3_name':day_3_name,
        'day_4_name':day_4_name,
        'day_5_name':day_5_name
        
    }
    return render(request, 'adminpanel/admin_dashboard.html', context)



def admin_category(request):
    if 's_email' in request.session:
        categories = Category.objects.all().order_by('-id')
        paginator = Paginator(categories,2)
        page = request.GET.get('page')
        paged_categories = paginator.get_page(page)
        context = {
            'categories':  paged_categories
        }
        return render(request, 'adminpanel/admin_category.html', context)
    else:
        return redirect('adminlogin')


def admin_products(request):
    if 's_email' in request.session:
        products = Product.objects.all().order_by('-id')
        paginator = Paginator(products,3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)

        context = {
            'products': paged_products
        }
        return render(request, 'adminpanel/admin_products.html', context)
    else:
        return redirect('adminlogin')


def users(request):
    users = CustomUser.objects.exclude(is_staff=True).order_by('-id')
    paginator = Paginator(users,5)
    page = request.GET.get('page')
    paged_users = paginator.get_page(page)
    context = {
        'users': paged_users

    }
    return render(request, 'adminpanel/users.html', context)


def adminlogout(request):
    if 's_email' in request.session:
        request.session.flush()
    auth.logout(request)
    return redirect('adminlogin')


def blockuser(request, id):
    user = CustomUser.objects.get(id=id)
    if user.is_active:
        user.is_active = False
        user.save()
        messages.success(request, 'User Successfully blocked!')

    else:
        user.is_active = True
        user.save()
        messages.success(request, 'User Successfully unblocked!')

    return redirect('users')


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():

            form.save()

            return redirect('admin_category')
        else:

            return redirect('add_category')
    else:
     form = CategoryForm()
     context = {
        'form': form
     }
     return render(request, 'adminpanel/add_category.html', context)


def admin_addproducts(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return redirect('admin_products')
        else:

            return redirect('admin_addproducts')
    else:
      form = ProductForm()
      context = {
        'form': form
      }
    return render(request, 'adminpanel/admin_addproducts.html', context)


def delete_category(request, id):
    dlt = Category.objects.get(pk=id)
    dlt.delete()
    return redirect('admin_category')


def delete_products(request, id):
    dlt = Product.objects.get(pk=id)
    dlt.delete()
    return redirect('admin_products')


def update_category(request, id):
    if request.method == 'POST':
        update = Category.objects.get(pk=id)
        form = Update_categoryForm(request.POST, instance=update)
        if form.is_valid():
            form.save()
            return redirect('admin_category')
        else:

            return redirect('update_category', id)
    else:
        update = Category.objects.get(pk=id)
        form = Update_categoryForm(instance=update)
        context = {
            'form': form
        }
        return render(request, 'adminpanel/update_category.html', context)


def update_products(request, id):
    if request.method == 'POST':
        update = Product.objects.get(pk=id)
        form = Update_ProductForm(request.POST, request.FILES, instance=update)
        if form.is_valid():
            form.save()
            return redirect('admin_products')
        else:

            return redirect('update_products', id)
    else:
        update = Product.objects.get(pk=id)
        form = Update_ProductForm(instance=update)
        context = {
            'form': form
        }
    return render(request, 'adminpanel/update_products.html', context)


def update_subcategory(request, id):
    if request.method == 'POST':
        update = Sub_Category.objects.get(pk=id)
        form = Update_subcategoryForm(request.POST, instance=update)
        if form.is_valid():
            form.save()
            return redirect('admin_subcategory')
        else:

            return redirect('update_subcategory', id)
    else:
        update = Sub_Category.objects.get(pk=id)
        form = Update_subcategoryForm(instance=update)
        context = {
            'form': form
        }
    return render(request, 'adminpanel/update_subcategory.html', context)


def add_subcategory(request):

    if request.method == 'POST':

        form = Sub_CategoryForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('admin_subcategory')
        else:

            return redirect('add_subcategory')

    form = Sub_CategoryForm()
    context = {
        'form': form
    }
    return render(request, 'adminpanel/add_subcategory.html', context)


def admin_subcategory(request):
    sub = Sub_Category.objects.all().order_by('-id')
    paginator = Paginator(sub,2)
    page = request.GET.get('page')
    paged_sub = paginator.get_page(page)

    context = {
        'sub': paged_sub,


    }
    return render(request, 'adminpanel/admin_subcategory.html', context)


def delete_subcategory(request, id):
    dlt = Sub_Category.objects.get(pk=id)
    dlt.delete()
    return redirect('admin_subcategory')

# Orders

def admin_orders(request):
    
    orders = Order.objects.filter(is_ordered=True).order_by('-id')
    context = {
        'orders':orders
    }
    
    return render (request,'adminpanel/admin_orders.html',context)



def update_order(request, id):
  if request.method == 'POST':
    order = get_object_or_404(Order, id=id)
    status = request.POST['status']
    print(status, id,  "status checking")
    order.status = status 
    order.save()
    if status  == "Delivered":
      try:
          payment = Payment.objects.get(payment_id = order.order_number, status = False)
          print(payment)
          if payment.payment_method == 'Cash on Delivery':
              payment.status = True
              payment.save()                                    
      except:
          pass
    order.save()
    return redirect('admin_orders')



def coupon(request):
    coupons = Coupon.objects.all().order_by('-id')
    paginator = Paginator(coupons,7)
    page= request.GET.get('page')
    paged_coupon = paginator.get_page(page) 
    context = {
        'coupons':paged_coupon
    }
    return render(request,'adminpanel/coupon.html',context)


def addCoupon(request):
    if request.method == 'POST':
      form = CouponForm(request.POST)
      if form.is_valid() :
         
         form.save()
         messages.success(request, 'Coupon added successfully.')
         return redirect('coupon')
      else:
         messages.error(request, 'Coupon already exisist!!!')
         return redirect('addCoupon')
      
    form = CouponForm()
    context={
        'form':form
    }
    return render(request,'adminpanel/add_coupon.html',context)  


def deleteCoupon(request,id):
    dlt = Coupon.objects.get(pk=id)
    dlt.delete()
    return redirect('coupon')

def updateCoupon(request,id):
    if request.method == 'POST':
        update = Coupon.objects.get(pk=id)
        form = CouponForm(request.POST,instance=update)
        if form.is_valid():
          form.save()
          return redirect('coupon')
        else:
            messages.error(request, 'Coupon already exsist!!!')
            return redirect('updateCoupon',id)
    else:
        update = Coupon.objects.get(pk=id)
        form = CouponForm(instance=update)
        context={
            'form':form
        }
    return render(request,'adminpanel/update_coupon.html',context)

 # variation
def variation(request):
    variation = Variations.objects.all().order_by('-id')
    paginator = Paginator(variation,7)
    page= request.GET.get('page')
    paged_variation = paginator.get_page(page) 
    context = {
        'variation' : paged_variation,
    }
    return render(request,'adminpanel/variations.html',context)


def delete_variation(request,id):
    dlt = Variations.objects.get(pk=id)
    dlt.delete()
    return redirect('variation')


def add_variation(request):
    if request.method == 'POST':
      form = VariationForm(request.POST)
      if form.is_valid() :
         
         form.save()
         messages.success(request, 'variation added successfully.')
         return redirect('variation')
      else:
         messages.error(request, 'variation already exisist!!!')
         return redirect('add_variation')
         
    form = VariationForm()
    context={
        'form':form
    }
    return render(request,'adminpanel/add_variations.html',context)

def update_variation(request,id):
    if request.method == 'POST':
        update =Variations.objects.get(pk=id)
        form = Update_VariationForm(request.POST,instance=update)
        if form.is_valid():
          form.save()
          return redirect('variation')
        else:
            messages.error(request, 'category already exsist!!!')
            return redirect('update_variation',id)
    else:
        update = Variations.objects.get(pk=id)
        form = Update_VariationForm(instance=update)
        context={
            'form':form
        }
    return render(request,'adminpanel/update_variations.html',context)




#sales report
def salesReport(request):
    year = datetime.now().year
    today = datetime.today()
    month = today.month
    years = []
    today_date=str(date.today())
    start_date=today_date
    end_date=today_date


    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        val = datetime.strptime(end_date, '%Y-%m-%d')
        end_date = val+timedelta(days=1)
        orders = Order.objects.filter(Q(created_at__lte=end_date),Q(created_at__gte=start_date),payment__status = 'True').values('user_order_page__product__product_name','user_order_page__product__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by('-total')
        paginator = Paginator(orders,1)
        page= request.GET.get('page')
        paged_report = paginator.get_page(page) 
       
    else:
        orders = Order.objects.filter(created_at__year = year,created_at__month=month,payment__status = 'True').values('user_order_page__product__product_name','user_order_page__product__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by('-total')
        paginator = Paginator(orders,7)
        page= request.GET.get('page')
        paged_report = paginator.get_page(page) 
        
    year = today.year
    for i in range (4):
        val = year-i
        years.append(val)

    


    context = {
        'orders':paged_report,
        'today_date':today_date,
        'years':years,
        'start_date':start_date,
        'end_date':end_date,
       
    }
    
    
    return render(request,'adminpanel/salesreport.html',context)



def salesReportMonth(request,id):
    orders = Order.objects.filter(created_at__month = id,payment__status = 'True').values('user_order_page__product__product_name','user_order_page__product__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by()
    paginator = Paginator(orders,7)
    page= request.GET.get('page')
    paged_report = paginator.get_page(page) 
    today_date=str(date.today())
    context = {
        'orders':paged_report,
        'today_date':today_date
    }
    return render(request,'adminpanel/salesreport_table.html',context)

def salesReportYear(request,id):
    orders = Order.objects.filter(created_at__year = id,payment__status = 'True').values('user_order_page__product__product_name','user_order_page__product__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by()
    paginator = Paginator(orders,7)
    page= request.GET.get('page')
    paged_report = paginator.get_page(page)    
    today_date=str(date.today())
    context = {
        'orders':paged_report,
        'today_date':today_date
    }
    return render(request,'adminpanel/salesreport_table.html',context) 



def pdfReport(request, start_date, end_date):
    year = datetime.now().year
    today = datetime.today()
    month = today.month
    
    if start_date == end_date:
      orders = Order.objects.filter(created_at__year = year,created_at__month=month,payment__status = 'True').values('user_order_page__product__product_name','user_order_page__product__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by('-total')
    else:
      orders = Order .objects.filter(Q(created_at__lte=end_date),Q(created_at__gte=start_date),payment__status = 'True').values('user_order_page__product__product_name','user_order_page__product__stock',total = Sum('order_total'),).annotate(dcount=Sum('user_order_page__quantity')).order_by('-total')
    
    template_path = 'adminpanel/salesreport_pdf.html'
    context = {'orders': orders,}
    
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=sales_report' + str(datetime.now()) +'.pdf'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
  
  
def excelReport(request, start_date, end_date):
    year = datetime.now().year
    today = datetime.today()
    month = today.month
    
    if start_date == end_date:
      orders = Order.objects.filter(created_at__year = year,created_at__month=month,payment__status = 'True').values_list('user_order_page__product__product_name', Sum('user_order_page__quantity'),'user_order_page__product__stock', Sum('order_total'))
    else:
      orders = Order.objects.filter(Q(created_at__lte=end_date),Q(created_at__gte=start_date),payment__status = 'True').values_list('user_order_page__product__product_name', Sum('user_order_page__quantity'),'user_order_page__product__stock', Sum('order_total'))
      
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=sales_report' + str(datetime.now()) +'.xls'
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Sales_report')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    
    columns = ['Item Name', 'Item sold', 'In stock', 'Amount Received']
    
    for col_num in range(len(columns)):
      ws.write(row_num, col_num, columns[col_num], font_style)
      
    font_style = xlwt.XFStyle()
    
    rows = orders
    
    for row in rows:
      row_num += 1

      for col_num in range(len(row)):
        ws.write(row_num, col_num, str(row[col_num]), font_style)
        
    wb.save(response)

    return response
    
    

  


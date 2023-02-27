from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import auth
from django.contrib.auth import login
from .models import CustomUser, UserProfile
from orders.models import Order, OrderProduct, Address
from django.contrib import messages
from .verify import send_otp, verify_otp
from my_cart.views import _cart_id
from my_cart.models import Cart, CartItem
import requests
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .forms import AddressForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserForm, UserProfileForm
from datetime import date
from datetime import timedelta


def signup(request):
    if 'email' in request.session:
        return redirect('home')
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        phone = request.POST['phone']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if CustomUser.objects.filter(email=email).exists():

                messages.warning(request, 'email already taken')
                print('email taken')
                return redirect('signup')
            elif CustomUser.objects.filter(phone=phone).exists():
                messages.warning(request, 'phone number already taken')
                print('phone taken')

                return redirect('signup')
            else:

                user = CustomUser.objects.create_user(
                    phone=phone, password=password1, email=email, first_name=firstname, last_name=lastname)
                user.save()
                messages.success(request, 'Successfully signed up!')
                print('user created')

            return redirect('login')

        else:
            messages.error(request, 'password not matching')
            print('password not matching')
            return redirect('signup')
    else:

        return render(request, 'accounts/signup.html')


def login(request):
    if 'email' in request.session:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                try:
                    cart = Cart.objects.get(cart_id=_cart_id(request))
                    is_cart_item_exists = CartItem.objects.filter(
                        cart=cart).exists()
                    if is_cart_item_exists:
                        cart_item = CartItem.objects.filter(cart=cart)

                        # getting the product variations by cart id
                        product_variation = []
                        for item in cart_item:
                            variation = item.variations.all()
                            product_variation.append(list(variation))

                        # get the cart items from the user to access his product variations
                        cart_item = CartItem.objects.filter(user=user)

                        ex_var_list = []
                        id = []
                        for item in cart_item:
                            existing_variation = item.variations.all()
                            ex_var_list.append(list(existing_variation))
                            id.append(item.id)
                        # product_variation=[1,2,3,4,6]
                        # ex_var_list=[4,6,3,5]

                        for pr in product_variation:
                            if pr in ex_var_list:
                                index = ex_var_list.index(pr)
                                item_id = id[index]
                                item = CartItem.objects.get(id=item_id)
                                item.quantity += 1
                                item.user = user
                                item.save()
                            else:
                                cart_item = CartItem.objects.filter(cart=cart)
                                for item in cart_item:
                                    item.user = user
                                    item.save()

                except:
                    pass
                request.session['email'] = email

                auth.login(request, user)
                messages.success(request, 'Successfully logged in!')
                url = request.META.get('HTTP_REFERER')
                try:
                    query = requests.utils.urlparse(url).query

                    # next=/cart/checkout/
                    params = dict(x.split('=')for x in query.split('&'))
                    if 'next' in params:
                        nextPage = params['next']
                        return redirect(nextPage)

                except:
                    return redirect('home')
            else:

                messages.error(request, 'You are Blocked !!')
                return redirect('login')
        else:
            messages.error(request, 'Invalid login')
            return redirect('login')
    else:

        return render(request, 'accounts/login.html')


def logout(request):
    if 'email' in request.session:
        request.session.flush()
    auth.logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('/')


def mobile_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        phone = request.POST['phone']
        if CustomUser.objects.filter(phone=phone).exists():
            request.session['phone'] = phone
            send_otp(phone)
            print('number exist')
            return redirect('verify_codelogin')
        else:
            messages.error(request, 'invalid mobile number!!')
            return redirect('mobile_login')
    else:
        return render(request, 'accounts/mobile_login.html')


def verify_codelogin(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        otp = request.POST.get('otp')
        mobile = request.session['phone']
        user = CustomUser.objects.get(phone=mobile)
        verify = verify_otp(mobile, otp)
        print(verify)
        if verify:
            if user.is_active:
                auth.login(request, user)
                print('logged in')
                return redirect('home')
            else:
                print('user blocked')
                messages.error(request, 'You are blocked!!')
                return redirect('login')

        else:
            messages.error(request, 'Incorrect OTP, try again!!')
            print('incorrect otp')
            return redirect('verify_codelogin')
    else:

        return render(request, 'accounts/verify_code.html')


@login_required(login_url='login')
def user_dashboard(request):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    user = request.user
    orders_count = orders.count()
    try:
        userprofile = UserProfile.objects.get(user_id=request.user.id)
    except UserProfile.DoesNotExist:
        userprofile = UserProfile.objects.create(user_id=request.user.id)
    context = {
        'orders_count': orders_count,
        'user': user,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/user_dashboard.html', context)


@login_required(login_url='login')
def edit_profile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = CustomUserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your Profile has been updated')
            return redirect('edit_profile')

        else:
            return redirect('edit_profile')
    else:
        user_form = CustomUserForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/edit_profile.html', context)


@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        user = CustomUser.objects.get(email__exact=request.user.email)
        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request, 'Password updated successfully')
                return redirect('change_password')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_password')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('change_password')
    return render(request, 'accounts/change_password.html')


@login_required(login_url='login')
def my_orders(request):
    orders = Order.objects.filter(user=request.user,is_ordered=True).order_by('-id')
    paginator = Paginator(orders,8)
    page= request.GET.get('page')
    paged_users = paginator.get_page(page)
    today = date.today()
    for order in orders:
     add = order.updated_at + timedelta(days=7)

    context = {
       'orders': paged_users, 
       'today':today,
       'add':add,
    }
    return render(request, 'accounts/my_orders.html', context)


@login_required(login_url='login')
def order_detail(request,order_id):
    order_detail = OrderProduct.objects.filter(order__order_number=order_id)
    orders = Order.objects.get(order_number=order_id)
    total=0
    for i in order_detail:
           total += i.product_price * i.quantity
    tax = (2*total)/100
    shipping = (2*total)/100
    print('check')
    
    
    context = {
        'order_detail':order_detail,
        'orders':orders,
        'total':total,
        'tax':tax,
        'shipping':shipping,
       
    }
    return render(request, 'accounts/order_detail.html', context)


@login_required(login_url='login')
def myAddress(request):
  current_user = request.user
  address = Address.objects.filter(user=current_user)
  paginator = Paginator(address,3)
  page= request.GET.get('page')
  paged_address = paginator.get_page(page)
  
  context = {
    'address':paged_address,
  }
  return render(request, 'accounts/myAddress.html', context)


@login_required(login_url='login')
def addAddress(request):
    if request.method == 'POST':
        form = AddressForm(request.POST, request.FILES,)
        if form.is_valid():
            print('form is valid')
            detail = Address()
            detail.user = request.user
            detail.first_name = form.cleaned_data['first_name']
            detail.last_name = form.cleaned_data['last_name']
            detail.phone = form.cleaned_data['phone']
            detail.email = form.cleaned_data['email']
            detail.address_line_1 = form.cleaned_data['address_line_1']
            detail.address_line_2 = form.cleaned_data['address_line_2']
            detail.state = form.cleaned_data['state']
            detail.country = form.cleaned_data['country']
            detail.city = form.cleaned_data['city']
            detail.save()
            messages.success(request, 'Address added Successfully')
            return redirect('myAddress')
        else:
            messages.success(request, 'Form is Not valid')
            return redirect('myAddress')
    else:
        form = AddressForm()
        context = {
            'form': form
        }
    return render(request, 'accounts/addAddress.html', context)


@login_required(login_url='login')
def deleteAddress(request, id):
    address = Address.objects.get(id=id)
    messages.success(request, "Address Deleted")
    address.delete()
    return redirect('myAddress')


@login_required(login_url='login')
def editAddress(request, id):
    address = Address.objects.get(id=id)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address Updated Successfully')
            return redirect('myAddress')
        else:
            messages.error(request, 'Invalid Inputs!!!')
            return redirect('myAddress')
    else:
        form = AddressForm(instance=address)

    context = {
        'form': form,
    }
    return render(request, 'accounts/editAddress.html', context)


# checkout
def deleteCheckoutAddress(request, id):
    address = Address.objects.get(id=id)
    messages.success(request, "Address Deleted")
    address.delete()
    return redirect('checkout')


def AddCheckoutAddress(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            print('form is valid')
            detail = Address()
            detail.user = request.user
            detail.first_name = form.cleaned_data['first_name']
            detail.last_name = form.cleaned_data['last_name']
            detail.phone = form.cleaned_data['phone']
            detail.email = form.cleaned_data['email']
            detail.address_line_1 = form.cleaned_data['address_line_1']
            detail.address_line_2 = form.cleaned_data['address_line_2']
            detail.state = form.cleaned_data['state']
            detail.country = form.cleaned_data['country']
            detail.city = form.cleaned_data['city']
            detail.save()
            messages.success(request, 'Address added Successfully')
            return redirect('checkout')
        else:
            messages.success(request, 'Form is Not valid')
            return redirect('checkout')

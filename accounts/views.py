import csv
import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import UpdateForm, CreateUserForm, EditProfile, ProfileForm, OrderForm
from .models import *


def register_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was successfully created for' + user)
                return redirect('login')

        context = {'form': form}
        return render(request, 'accounts/register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or Password is incorrect')
        return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    orders = Order.objects.order_by('order')
    customer = Customer.objects.all()
    total_order = orders.count()
    total_customers = customer.count()
    total_delivered = orders.filter(status='Delivered').count()
    product = Product.objects.all()
    products = product.count()
    context = {
        'orders': orders,
        'total_customers': total_customers,
        'total_orders': total_order,
        'total_delivered': total_delivered,
        'products': products
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='login')
def update(request, id):
    order = Order.objects.get(id=id)
    form = UpdateForm()
    if request.method == 'POST':
        form = UpdateForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/update.html', context)


@login_required(login_url='login')
def delete(request, id):
    order = Order.objects.get(id=id)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {'order': order}
    return render(request, 'accounts/delete.html', context)


def export_csv(request):
    now = datetime.datetime.now()
    date = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Order List ' + str(date) + '.csv"'
    writer = csv.writer(response)
    writer.writerow(['Order ID', 'Date', 'Status', 'Customer Name', 'Customer Email', 'Phone', 'Item quantity',
                     'Item' 'Coupon/Discount', 'New Amount(Tk)', 'Shipping Address', 'Payment Status'])
    orders = Order.objects.all()

    for order in orders:
        writer.writerow([order.order, order.date_created, order.status, order.customer.name, order.customer.email,
                         order.customer.phone, order.quantity, order.product, order.coupon, order.product.price,
                         order.shipping_address, order.payment])

    return response


@login_required(login_url='login')
def customer(request, id):
    customer = Customer.objects.get(id=id)
    orders = customer.order_set.all()
    context = {
        'orders': orders,
        'customer': customer
    }
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
def profile(request):
    user = request.user
    context = {
        'user': user
    }
    return render(request, 'accounts/profile.html', context)


@login_required(login_url='login')
def update_profile(request):
    profile = Profile.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = EditProfile(request.POST, instance=request.user)
        profle_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid() and profle_form.is_valid():
            user_form = form.save()
            custom_form = profle_form.save(False)
            custom_form.user = user_form
            custom_form.save()
            messages.success(request, 'user profile has been updated')
            return redirect('/')
        else:
            messages.error(request, 'Submission Error')
    if request.method == 'GET':
        form = EditProfile(instance=request.user)
        profle_form = ProfileForm(instance=profile)
        context = {
            'form': form,
            'profile_form': profle_form
        }
        return render(request, 'accounts/update_profile.html', context)


@login_required(login_url='login')
def all_customer(request):
    customer = Customer.objects.all()
    context = {
        'customers': customer
    }
    return render(request, 'accounts/all_customer.html', context)


@login_required(login_url='login')
def all_product(request):
    product = Product.objects.all()
    context = {
        'products': product
    }
    return render(request, 'accounts/all_product.html', context)


@login_required(login_url='login')
def add_order(request):
    order = Order.objects.all()
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'accounts/add_order.html', context)

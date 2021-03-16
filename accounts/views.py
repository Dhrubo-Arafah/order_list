import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import csv
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import UpdateForm, CreateUserForm
from .models import *
from .filters import OrderFilter


def register_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was successfully created for' +user)
                return redirect ('login')

        context = {'form': form}
        return render(request, 'accounts/register.html', context)

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method=='POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            user=authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or Password is incorrect')
        return render(request, 'accounts/login.html')

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
    product=Product.objects.all()
    products=product.count()
    context = {
        'orders': orders,
        'total_customers': total_customers,
        'total_orders': total_order,
        'total_delivered': total_delivered,
        'products':products
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

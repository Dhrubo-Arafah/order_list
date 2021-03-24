from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


class Customer(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.EmailField()
    address = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
        ('Electronic Devices', 'Electronic Devices'),
        ('Home & Lifestyle', 'Home & Lifestyle'),
        ('Health & Beauty', 'Health & Beauty'),
    )
    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    description = models.CharField(max_length=500, null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Delivered', 'Delivered'),
        ('Shipped', 'Shipped'),
        ('Cancelled', 'Cancelled'),
    )
    PAYMENT = (
        ('Paid', 'Paid'),
        ('Expired', 'Expired'),
        ('Pending', 'Pending'),
    )
    order = models.CharField(max_length=200, null=True)
    quantity = models.CharField(max_length=200, null=True)
    coupon = models.CharField(max_length=200, null=True)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    shipping_address = models.CharField(max_length=200, null=True)
    payment = models.CharField(max_length=200, null=True, choices=PAYMENT)

    def __str__(self):
        return self.order


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    profile_pic = models.ImageField(upload_to='image/')

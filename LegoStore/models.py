import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


# Create your models here.

class Sale(models.Model):
    name = models.CharField(max_length=100)
    begin_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
    description = models.TextField()
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    
    class Meta:
        default_permissions = ('view')
        permissions = [
            ('view_special_offer', 'View Special Offer')
        ]

class Order(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    sale = models.ForeignKey('Sale', on_delete=models.CASCADE, null=True)
    
    def get_absolute_url(self):
        return reverse('category_detail', args=[str(self.id)])

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)    
    stock_quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)
    orders = models.ManyToManyField(Order, through='OrderProduct')
    
    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])
    
    class Meta:
        default_permissions = ('view')


class Review(models.Model):
    rating = models.SmallIntegerField()
    comment = models.TextField()
    review_date = models.DateTimeField(auto_now_add=True)
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Inventory(models.Model):
    quantity_in_stock = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class OrderProduct(models.Model):
    quantity = models.IntegerField()
    price_at_order = models.DecimalField(max_digits=10, decimal_places=2)
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    county = models.CharField(max_length=100, blank=True)
    
    code = models.CharField(max_length=100, null=True)
    email_confirmed = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)
    
    class Meta:
        permissions = [
            ('moderator-permissions', 'Moderator Permissions'),
        ]
    
class LastProductViews(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    last_viewed = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if LastProductViews.objects.filter(user=self.user).count() >= 5:
            oldest_view = LastProductViews.objects.filter(user=self.user).order_by('last_viewed').first()
            oldest_view.delete()
        super().save(*args, **kwargs)
    

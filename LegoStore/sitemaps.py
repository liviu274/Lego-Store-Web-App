from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Category, Product, Review, CustomUser, Sale

class CategorySitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.8
    
    def items(self):
        return Category.objects.all()
    
    def sale(self, obj : Category) -> Sale:
        return obj.sale
    
class ProductSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.8

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.created_at

# class ReviewSitemap(Sitemap):
#     changefreq = 'weekly'
#     priority = 0.6

#     def items(self):
#         return Review.objects.all()

#     def lastmod(self, obj):
#         return obj.review_date

# class CustomUserSitemap(Sitemap):
#     changefreq = 'monthly'
#     priority = 0.5

#     def items(self):
#         return CustomUser.objects.all()

#     def lastmod(self, obj):
#         return obj.date_joined

class ViewsSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return [
            'home', 
            'showProducts', 
            'filterProducts', 
            'contact', 
            'addReview', 
            'testMessage', 
            'register', 
            'loginView', 
            'passwordChange', 
            'logoutView', 
            'loggedIn', 
            'special_offer', 
            'hasSpecialOffer'
        ]
    
    def location(self, item):
        # Returneaza URL-ul pentru fiecare item
        # Atentie, acestea trebuie sa aiba name specificat in urls.py
        return reverse(item)
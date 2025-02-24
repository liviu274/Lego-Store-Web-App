from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from . import views
from .sitemaps import *

sitemaps = {
    'category' : CategorySitemap,
    'produit' : ProductSitemap,
    'static' : ViewsSitemap,
}


urlpatterns = [
    # View urls
    path('', views.home, name='home'),
    path('products/', views.showProducts, name='showProducts'),
    path('filter_products/', views.filterProducts, name='filterProducts'),
    path('contact/', views.contact, name='contact'),
    path('add-review/', views.addReview, name='addReview'),
    path('test-message/', views.testMessage, name='testMessage'),
    path('register/', views.register, name='register'),
    path('login/', views.loginView, name='loginView'),
    path('password_change/', views.passwordChange, name='passwordChange'),
    path('logout/', views.logoutView, name='logoutView'),
    path('logged_in/', views.loggedIn, name='loggedIn'),
    path('confirm_email/<str:code>/', views.confirmRegistration, name='confirmRegistration'),
    path('sales/', views.addSale, name='addSale'),
    path('special_offer/', views.special_offer, name='special_offer'),
    path('has_special_offer/', views.hasSpecialOffer, name='hasSpecialOffer'),
    path('category/<int:id>/', views.category_detail, name='category_detail'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('basket/', views.basket, name='basket'),
    
    
    # Sitemap urls
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

]
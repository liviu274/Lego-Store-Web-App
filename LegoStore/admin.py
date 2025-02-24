from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from .models import *
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    filter = ['description', 'name']
    search_fields = ['name', 'product']
    fields = ['name', 'description']

class ProductAdmin(admin.ModelAdmin):
    search_fields = ['name',  'price']
    list_filter = ['price']

class ReviewAdmin(admin.ModelAdmin):
    search_fields = ['rating', 'comment', 'review_date', 'product']
    fieldsets = (
        ('Rating and Product', {'fields' : ('rating', 'product',)}),
        ('Comments', {'fields' : ('comment',),
                    'classes' : ('collapse',)
                    }),
    )

class InventoryAdmin(admin.ModelAdmin):
    search_fields = ['last_updated']
    

class OrderProductAdmin(admin.ModelAdmin):
    search_fields = ['quantity', 'price_at_order']

class OrderAdmin(admin.ModelAdmin):
    search_fields = ['order_date', 'total_price', 'status']
    
class LastProductViewsAdmin(admin.ModelAdmin):
    search_fields = ['product', 'user', 'view_date']
    
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone', 'zip_code', 'address', 'city', 'county')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important info', {'fields': ('last_login', 'date_joined', 'email_confirmed', 'blocked')}),
    )

    def get_form(self, request, obj=None, **kwargs):
        print(f'THIS IS THE USERNAME: {request.user.username}')
        if not request.user.has_perm('LegoStore.moderator-permissions'):
            raise PermissionDenied
        return super().get_form(request, obj, **kwargs)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Inventory, InventoryAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(LastProductViews, LastProductViewsAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.site_header = 'Site Administration'
admin.site.site_title = 'Lego Store Admin'
admin.site.index_title = 'Lego Store Admin Dashboard'

# Generated by Django 5.1.1 on 2025-01-14 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LegoStore', '0005_sale_lastproductviews_category_sale'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'default_permissions': 'view'},
        ),
        migrations.AlterModelOptions(
            name='sale',
            options={'default_permissions': 'view', 'permissions': [('view_special_offer', 'View Special Offer')]},
        ),
    ]

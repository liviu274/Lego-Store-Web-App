# Generated by Django 5.1.1 on 2024-12-18 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LegoStore', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='cod',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='email_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]

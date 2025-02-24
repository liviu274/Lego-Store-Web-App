from django import forms
from django.core.exceptions import ValidationError
import datetime
from .models import Review, Product, CustomUser, Category, Sale
from decimal import Decimal
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.core.mail import mail_admins
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
import random
import string
import time
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth import get_user_model

PRICE_CHOICES =(
    (0, 'Any'),
    (1, '0-100'),
    (2, '100-250'),
    (3, '250-500'),
    (4, '500-1000'),
    (5, '1000+')
)

MESSAGE_CHOICES = (
    ('c', 'Complaint'),
    ('q', 'Question'),
    ('r', 'Review'),
    ('req', 'Request'),
    ('ap', 'Appointment')
)

def validateText(inputs:list[str]):
    for txt in inputs:
        if txt and txt[0].isupper():
            for word in txt.split():
                if not word.isalpha():
                    raise forms.ValidationError('Text must only contain letters and spaces')
        elif txt:
            raise forms.ValidationError('Text must start with uppercase!')
        
def mustStartWithUpperCase(inputs:list[str]):
    for txt in inputs:
        if txt and not txt[0].isupper():
            raise forms.ValidationError('Must start with uppercase')
        elif not txt:
            raise forms.ValidationError('Text is empty')

class ProductForm(forms.Form):
    name = forms.CharField(max_length=100, label='Name', required=False)
    description = forms.CharField(widget=forms.Textarea, max_length=500, label='Description', required=False)
    price = forms.ChoiceField(choices=PRICE_CHOICES, required=False)
    
class ContactForm(forms.Form):
    firstName = forms.CharField(required=False, label='First Name')
    lastName = forms.CharField(max_length=10, required=True, label='Last Name')
    birthDate = forms.DateTimeField(required=False, label='Birth Date')
    email = forms.EmailField(required=True, label='Email')
    confirmEmail = forms.EmailField(required=True, label='Confirm Email')
    messageType = forms.ChoiceField(choices=MESSAGE_CHOICES, label='Message Type')
    subject = forms.CharField(required=True, label='Subject')
    minWaitDays = forms.FloatField(min_value=1.0, label='Minimum Wait Days')
    message = forms.CharField(widget=forms.Textarea, help_text='It must only contain letters and spaces', label='Message')
    def clean_date(self):
        birthDate = self.cleaned_data.get('birthDate')
        if not birthDate:
            raise forms.ValidationError('Please enter your birth date')
        age = (datetime.now().date() - birthDate.date()).days / 365.25
        print(f"Sender age is: {age}")
        if age < 18:
            raise forms.ValidationError('You must be over 18!')
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        name = self.cleaned_data.get('firstName')
        words = message.split()
        mesLength = len(words)
        if mesLength < 5:
            raise forms.ValidationError('Your message is too short. It must habe at least 5 words!')
        elif mesLength > 100:
            raise forms.ValidationError('Your message is too long. It must have at most 100 words!')    
        for word in words:
            if word.startswith('http://') or word.startswith('https://'):
                raise forms.ValidationError('Links are not allowed in the message!')
        if words[-1] != name:
            print(words[-1], name)
            raise forms.ValidationError('The message must contain user signature! (first name as the last word)')
    
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        confirmEmail = cleaned_data.get('confirmEmail')
        if email and confirmEmail and email != confirmEmail:
            raise forms.ValidationError('Emails do not match')
        
        # Validate text correctitude
        
        message = cleaned_data.get('message')
        firstName = cleaned_data.get('firstName') # can be null by definition
        lastName = cleaned_data.get('lastName')
        
        validateText([message, firstName, lastName])
        
class ReviewForm(forms.ModelForm):
    productName = forms.CharField(max_length=100, help_text='It must be an existing product name!', label='product name')
    productPrice = forms.DecimalField(max_digits=10, decimal_places=2, help_text='It must not be more or less than 10 percent of the current product price!', label='price at order')
    class Meta:
        model = Review
        fields = ['rating', 'comment']

    def clean_productName(self):
        myName = self.cleaned_data.get('productName')
        print(f"input name is {myName}")
        productName = Product.objects.filter(name__iexact=myName)
        if productName:
            print(f"product name is {productName.first().name}")
        if not productName:
            print('raise validation product name')
            raise forms.ValidationError('Name does not correspound to any existing product')
        return myName
        
    # def clean_productPrice(self):
        
        
    def clean(self):
        cleaned_data = super().clean()
        myprice = cleaned_data.get('productPrice')
        myName = cleaned_data.get('productName')
        
        if myName and myprice is not None:
            product = Product.objects.filter(name__iexact=myName).first()
            if product:
                product_price = product.price
                lower_bound = product_price * Decimal('0.9')
                upper_bound = product_price * Decimal('1.1')
                if not (lower_bound <= myprice <= upper_bound):
                    print('raise validation product price')
                    raise forms.ValidationError('The price must be within 10 percent of the current product price!')
        
        comment = cleaned_data.get('comment')
        mustStartWithUpperCase([myName, comment])
        
        return cleaned_data

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'zip_code', 'address', 'city', 'county', 'password1', 'password2']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if not phone.isdigit(): 
            raise forms.ValidationError('Phone number must contain only digits.')
        return phone

    def clean_zip_code(self):
        zip_code = self.cleaned_data.get('zip_code')
        if not zip_code.isdigit():
            raise forms.ValidationError('Zip code must contain only digits.')
        return zip_code
    
    def clean_county(self):
        county = self.cleaned_data.get('county')
        if county and not county[0].isupper():
            raise forms.ValidationError('County must start with uppercase')
        return county
    
    @staticmethod
    def generate_random_string(length=100):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        
    def save(self, commit = True):
        user = super().save(commit=False)
        user.phone = self.cleaned_data['phone']
        user.zip_code = self.cleaned_data['zip_code']
        user.county = self.cleaned_data['county']
        user.code = self.generate_random_string()
        self.cleaned_data['code'] = user.code
        
        if commit:
            user.save()
        return user





class CustomAuthenticationForm(AuthenticationForm):
    stay_logged_in = forms.BooleanField(required=False, initial=False, label='Stay logged in')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.login_counter_key = 'login_counter'
        self.reset_interval = timedelta(minutes=2)
        self.reset_login_counter()

    def reset_login_counter(self):
        last_reset = cache.get('last_reset')
        now = timezone.now()
        if not last_reset or now - last_reset > self.reset_interval:
            cache.set(self.login_counter_key, 0, timeout=None)
            cache.set('last_reset', now, timeout=None)

    def increment_login_counter(self):
        counter = cache.get(self.login_counter_key, 0)
        counter += 1
        cache.set(self.login_counter_key, counter, timeout=None)

    def clean(self):
        cleaned_data = super().clean()
        stay_logged_in = cleaned_data.get('stay_logged_in')
        username = cleaned_data.get('username')
        
        self.increment_login_counter()

        if username == 'admin':
            mail_admins(
            subject='Cineva incearca sa ne fure site-ul',
            message=f'Cineva s-a logat cu admin',
            html_message=f'<p><strong style="color:red;">ATENTIE!</strong> cineva a incercat sa se logheze cu user admin</p>',
            fail_silently=False
        )
            
        user = CustomUser.objects.filter(username=username).first()
        if user and not user.email_confirmed:
            raise forms.ValidationError('Please confirm your email before logging in')
        
        login_counter = cache.get(self.login_counter_key, 0)
        if login_counter > 3:
            @receiver(user_logged_in)
            def get_user_ip(sender, request, user, **kwargs):
                ip = request.META.get('REMOTE_ADDR')
                return ip
            
            ip_address = get_user_ip(sender=None, request=self.request, user=None)
            mail_admins(
                subject='Suspect logins',
                message=f'The user with username: {username} having the following IP address {ip_address} has attempted 3 unsuscessfull logins in less than 3 minutes',
                html_message=f'<p><strong style="color:red;">WARNING!</strong>The user with username: {username} having the following IP address {ip_address} has attempted 3 unsuscessfull logins in less than 3 minutes</p>',
                fail_silently=False,
            )
            print('MAIL ADMINS 3 LOGINS WITHIN TIMER LIMITS')
        return cleaned_data
    
class CustomPasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label='Old Password')
    new_password1 = forms.CharField(widget=forms.PasswordInput, label='New Password')
    new_password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm New Password')

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError('The new passwords do not match')

        return cleaned_data
    
class SaleCreationForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['name', 'description', 'discount']
    
    subject = forms.CharField(max_length=100, label='Subject', required=True)
    duration = forms.IntegerField(min_value=1, label='Duration (days)')
    categories = forms.MultipleChoiceField(choices=[(c.id, c.name) for c in Category.objects.all()], label='Categories', initial='All', required=True)
    
    class CustomUserChangeForm(forms.ModelForm):
        class Meta:
            model = CustomUser
            fields = ['first_name', 'last_name', 'email', 'blocked']

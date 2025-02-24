from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Permission
from .models import Category, Product, LastProductViews
from .forms import *
from django.contrib import messages
from datetime import datetime
import os
import json
from django.contrib.auth import login, logout, update_session_auth_hash
from django.core.mail import send_mail, send_mass_mail
from django.template.loader import render_to_string
from datetime import timedelta
import logging

logger = logging.getLogger('LegoStore')
# Create your views here.   

def home(request):
    return render(request, 'homepage.html', {'user': request.user})

def special_offer(request):
    if not request.user.is_authenticated:
        context = {
            'title': 'You are not logged in!',
        }
        return HttpResponseForbidden(render_to_string('error403.html', context))
    user = request.user
    permission = Permission.objects.get(codename='view_special_offer')
    user.user_permissions.add(permission)
    return render(request, 'special_offer.html', {'user': request.user})

@login_required
@permission_required('LegoStore.view_special_offer', raise_exception=True)
def hasSpecialOffer(request):
    return HttpResponse(f'Success, user {request.user.username} has special offer!')


def showProducts(request):
    global logger
    
    logger.info('The old products page was accessed')
    messages.info(request, "Debug: this only prints some filters")
    return render(request, 'products.html',
    {
        'product_names': Product.objects.filter(name='Lego tractor').all(),
        'product_prices': Product.objects.filter(price__lte=400).all(),
    }
    )

price_high = 10000
price_low = 0

price_choices = {
    0 : (0, 10000),
    1 : (0, 100),
    2 : (100, 250),
    3 : (250, 500), 
    4 : (500, 1000),
    5 : (1000, 10000)
}

formName = ''
formDescription = ''

def filterProducts(request):
    
    global price_low, price_high, formName, formDescription, logger
    messages.warning(request, "You need to enteer a valid product name!")
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            print('FORM IS VALID!')
            formName = form.cleaned_data['name']
            print(f"formName is: {formName}")
            formDescription = form.cleaned_data['description']
            formPrice = int(form.cleaned_data['price'])
            print(formPrice)
            price_low = price_choices[formPrice][0]
            price_high = price_choices[formPrice][1]
            return redirect('/project/filter_products')
    else:
        form = ProductForm()
        # print(f"PRICE LOW {price_low} : PRICE_HIGH {price_high}")
        logger.debug(f'PRICE LOW {price_low} : PRICE_HIGH {price_high}')
        return render(request, 'product_form.html', {
            'form': form,
            'products': Product.objects.filter(price__lte=price_high,
                                            price__gte=price_low,
                                            name__contains=formName,
                                            description__contains=formDescription),
            })

def contact(request):
    global logger
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            print('FORM IS VALID')
            logger.debug('FORM IS VALID: Contact Form is Vald')
            messages.info(request, "Form has been sent")
            # handel form submission
            messages.success(request, 'Your form has been submitted successfully')
            birthDate = form.cleaned_data['birthDate']
            
            today = datetime.today()
            age_years = today.year - birthDate.year
            age_months = today.month - birthDate.month

            if today.day < birthDate.day:
                age_months -= 1

            if age_months < 0:
                age_years -= 1
                age_months += 12

            age = f"{age_years} years and {age_months} months"
            
            mymes = form.cleaned_data['message']
            print(form.cleaned_data['firstName'])
            print(mymes)
            # mymes = mymes.strip()
            print(form.cleaned_data['messageType'])
            form_data = {
                'firstName': form.cleaned_data['firstName'],
                'lastName': form.cleaned_data['lastName'],
                'age': age,
                'email': form.cleaned_data['email'],
                'messageType': form.cleaned_data['messageType'],
                'subject': form.cleaned_data['subject'],
                'minWaitDays': form.cleaned_data['minWaitDays'],
                'message': mymes
            }
            
            # Ensure the messages directory exists
            messages_dir = os.path.join(os.path.dirname(__file__), 'messages')
            os.makedirs(messages_dir, exist_ok=True)

            # Create a unique filename based on the current timestamp
            filename = os.path.join(messages_dir, f"message_{datetime.now().strftime('%Y%m%d%H%M%S')}.json")

            # Save the form_data to the JSON file
            with open(filename, 'w') as json_file:
                json.dump(form_data, json_file, indent=4)
            
            return redirect('/project/contact')
        else:
            messages.error(request, "Form is not valid")
            print('FORM IS NOT VALID')
        
    else:
        form = ContactForm()
    return render(request, 'contact_form.html', {'form': form})

def addReview(request):
    global logger
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            print('FORM IS VALID!')
            messages.info(request, "Formularul a fost trimis cu succes :) ")
            myReview = form.save(commit=False)
            productPrice = form.cleaned_data['productPrice']
            productName = form.cleaned_data['productName']
            product = Product.objects.filter(name__iexact=productName)
            print(product)
            myReview.comment = myReview.comment + ' ' + str(productPrice) + ' '
            myReview.comment = myReview.comment + productName
            myReview.product_id=product.first().id
            myReview.save()
            logger.info('ADD REVIEW: Review added successfully!')
            messages.success(request, 'Ai fost redirectionat cu succes')
            return redirect('/project/')
        else:
            print('FORM IS NOT VALID')
            messages.error(request, "!!! Eroare raspunsul nu este valid")
            return render(request, 'review_form.html', {'form': form})
    else:
        form = ReviewForm()
        return render(request, 'review_form.html', {'form': form})
    

def sendRegistrationMail(first_name, last_name, username, confirmation_link):
    context = {'first_name': first_name, 'last_name': last_name, 'username': username, 'confirmation_link': confirmation_link}
    send_mail(
        subject='Confirm registration!',
        message=' ',
        html_message=render_to_string('register_confirmation_mail.html', context),  # HTML content
        from_email='test.tweb.node@gmail.com',
        recipient_list=['legostore.project.liviu@gmail.com'],
        fail_silently=False,
    )


def register(request):
    global logger
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            confirmation_link = "http://127.0.0.1:8000/project/confirm_email/"
            confirmation_link += form.cleaned_data['code']
            sendRegistrationMail(first_name, last_name, username, confirmation_link)
            messages.info(request, "User created successfully, please check your email for confirmation")
            return redirect('/project/')  # Redirect to a success page (home)
    else:
        form = CustomUserCreationForm()
        logger.warning('REGISTER: Registration failed')
    return render(request, 'userCreationForm.html', {'form': form})

def confirmRegistration(request, code):
    global logger
    user = CustomUser.objects.filter(code=code).first()
    if user:
        user.email_confirmed = True
        user.save()
        logger.warning(f'CONGIRM_REGISTRATION: User {user.username} email_confirmed set to True!')
        return HttpResponse('User confirmed')
        
    else:
        logger.error('CONGIRM_REGISTRATION: Invalid confirmation code')
        return HttpResponse('Invalid confirmation code')

def loginView(request):
    global logger
    if 'username' in request.session and request.session.get_expiry_age() > 0:
        messages.info(request, "You are already logged in")
        print(f"expires in {request.session.get_expiry_age()}")
        logger.error('LOGIN: User allready logged in tries a new login')
        return redirect('/project/logged_in')

    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST, request=request)
        if form.is_valid():
            user = form.get_user()
            if user.blocked:
                messages.error(request, 'Your account has been blocked')
                logger.critical(f'LOGIN: User {user.username} is blocked')
                context = {
                    'title': 'Error logging in',
                    'username' : user.username,
                    'custom_message': 'Your account has been blocked'
                }
                return HttpResponseForbidden(render_to_string('error403.html', context))               
            login(request, user)
            
            # Save user data in session
            request.session['username'] = user.username
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            request.session['email'] = user.email
            request.session['phone'] = user.phone
            request.session['zip_code'] = user.zip_code
            request.session['address'] = user.address
            request.session['city'] = user.city
            request.session['county'] = user.county
            
            if not form.cleaned_data.get('stay_logged_in'):
                print('Session will expire when the browser is closed')
                request.session.set_expiry(1)
            else:
                request.session.set_expiry(24*60*60)  # 24 hours in seconds
            return redirect('/project/logged_in')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def loggedIn(request):
    if not request.user.is_authenticated:
        messages.info(request, 'You are not logged in')
        return redirect('/project/login')
    
    username = request.session.get('username')
    first_name = request.session.get('first_name')
    last_name = request.session.get('last_name')
    email = request.session.get('email')
    phone = request.session.get('phone')
    zip_code = request.session.get('zip_code')
    address = request.session.get('address')
    city = request.session.get('city')
    county = request.session.get('county')
    return render(request, 'logged_in.html', {'username': username, 'first_name': first_name, 'last_name': last_name, 'email': email, 'phone': phone, 'zip_code': zip_code, 'address': address, 'city': city, 'county': county})

def passwordChange(request):
    global logger
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            logger.critical(f'PASSWORD_CHANGE: User {request.user.username} password changed!')
            update_session_auth_hash(request, request.user)
            request.session.flush()
            request.session.set_expiry(0)
            messages.success(request, 'Password changed successfully.')
            return redirect('/project/')
        else:
            messages.error(request, 'There are some unhandele errors')
            logger.critical('Password changed failed!')
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, 'password_change.html', {'form': form})
    
def logoutView(request):
    user = request.user
    permission = Permission.objects.get(codename='view_special_offer')
    user.user_permissions.remove(permission)
    logout(request)
    request.session.flush()
    request.session.set_expiry(0)
    return redirect('/project/login')

# def userLoggedIn(request):
#     return render(request, 'logged_in.html')

def testMessage(request):
    messages.debug(request, "Acesta este un mesaj de depanare. :( ")
    messages.info(request, "Acesta este un mesaj informativ. :) ")
    messages.success(request, "Actiunea a avut succes! :D ")
    messages.warning(request, "Acesta este un avertisment. :| ")
    messages.error(request, "A aparut o eroare! >:((  ")
    return render(request, 'standard_template.html')

K = 2

def addSale(request):
    if not request.user.has_perm('LegoStore.add_sale'):
        context = {
            'title': 'Error adding sale',
            'username' : request.user.username,
            'custom_message': 'You do not have the permission to add a sale'
        }
        return HttpResponseForbidden(render_to_string('error403.html', context))
    
    global K
    if request.method == 'POST':
        form = SaleCreationForm(data=request.POST)
        if form.is_valid():
            mySale = form.save(commit=False)
            mySale.begin_date = datetime.now()
            mySale.end_date = mySale.begin_date + timedelta(days=form.cleaned_data['duration'])
            mySale.save()
            messages.success(request, 'Sale created successfully.')

            # send mass mail logic
            
            userViewCounter = dict()
            selected_categories = form.cleaned_data['categories']
            for categoryID in selected_categories:
                category = Category.objects.filter(id=categoryID).first()
                print(category.name, categoryID)
                category.sale = mySale
                category.save()
                
                for view in LastProductViews.objects.filter(product__category=category).all():
                    if view.user in userViewCounter:
                        userViewCounter[view.user] += 1
                    else:
                        userViewCounter[view.user] = 1
                
                liableusers = []
                if userViewCounter.items():
                    for user, views in userViewCounter.items():
                        if views >= K:
                            liableusers.append(user)

            messageTechnic = render_to_string('sale_lego_technic_mail.html', {'subject': mySale.name,
                                                                            'expiry_date': mySale.end_date})
            messageCreator = render_to_string('sale_lego_creator_mail.html', {'subject': mySale.name,
                                                                            'expiry_date': mySale.end_date})
            
            emails = [user.email for user in liableusers]
            print(liableusers)
            print(userViewCounter)
            emails.append('test.tweb.node@gmail.com')
            
            datadict = {
                'Technic' : (mySale.name, messageTechnic, 'test.tweb.node@gmail.com', emails),
                'Creator' : (mySale.name, messageCreator, 'test.tweb.node@gmail.com', emails),
            }
            
            datalist = []
            
            categoryNames = set()
            
            for categoryID in selected_categories:
                category = Category.objects.filter(id=categoryID).first()
                categoryNames.add(category.name)
            
            if 'Technic' in categoryNames and 'Creator' in categoryNames:
                datalist.append(datadict['Technic'])
                datalist.append(datadict['Creator'])
                send_mass_mail(datalist)
            elif 'Technic' in categoryNames:
                datalist.append(datadict['Technic'])
                send_mass_mail(datalist)
            elif 'Creator' in categoryNames:
                datalist.append(datadict['Creator'])
                send_mass_mail(datalist)
                
                
                
            # for categoryID in selected_categories:
            #     category = Category.objects.filter(id=categoryID).first()
            #     if category.name == 'Technic':
            #         send_mass_mail(datadict['Technic'])
            #     if category.name == 'Creator':
            #         send_mass_mail(datadict['Creator'])
            
            return redirect('/project/')
        else:
            messages.error(request, 'There are some unhandele errors')
    else:
        form = SaleCreationForm()
        for field in form:
            print(field.name)
    return render(request, 'sales_form.html', {'form': form})

def category_detail(request, id):
    category = get_object_or_404(Category, id=id)
    return render(request, 'category_detail.html', {'category': category})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})

def basket(request):
    return render(request, 'basket.html')
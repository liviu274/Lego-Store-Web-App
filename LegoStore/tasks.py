import schedule
import time
import django
import os

# load project settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniProject.settings')
django.setup()

from django.utils import timezone
from .models import CustomUser

from django.core.mail import send_mail
from django.template.loader import render_to_string

def task_delete_not_confirmed_users():
    print("TASK DELEETE NOT CONFIRMED USERS")
    users = CustomUser.objects.all()
    for user in users:
        if not user.email_confirmed:
            user.delete()
    
def send_newsletter_to_user(user):
    subject = 'Exclusive Newsletter from LegoStore'
    message = ' '
    html_message = render_to_string('newsletter_template.html', {'user': user})
    from_email = 'test.tweb.node@gmail.com'
    recipient_list = ['legostore.project.liviu@gmail.com']

    send_mail(
        subject=subject,
        message=message,
        html_message=html_message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False,
    )
    
def task_send_newsletter(min_minutes=1):
    print("TASK SEND NEWSLETTER")
    now = timezone.now()
    users = CustomUser.objects.filter(date_joined__lte=now - timezone.timedelta(minutes=min_minutes))
    for user in users:
        # Assuming you have a function send_newsletter_to_user
        send_newsletter_to_user(user)
        
# Task 1 reminder
def task_send_reminder_email():
    print("TASK SEND REMINDER EMAIL")
    users = CustomUser.objects.filter(is_active=True)
    for user in users:
        subject = 'Reminder from LegoStore'
        message = 'This is a reminder email.'
        from_email = 'test.tweb.node@gmail.com'
        recipient_list = ['legostore.project.liviu@gmail.com']

        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            fail_silently=False,
        )

# Task 2: Weekly report at 8:00 AM
def task_send_daily_report():
    print("TASK SEND DAILY REPORT")
    users = CustomUser.objects.filter(is_active=True)
    subject = 'Daily Report from LegoStore'
    message = 'This is the daily report.'
    from_email = 'test.tweb.node@gmail.com'
    recipient_list = ['legostore.project.liviu@gmail.com']

    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        fail_silently=False,
    )



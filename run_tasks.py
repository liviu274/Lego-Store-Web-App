import schedule
import time
import django
import os
import sys
from LegoStore import tasks
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniProject.settings')
django.setup()

def run_scheduler():
    schedule.every(1).minutes.do(tasks.task_delete_not_confirmed_users)
    schedule.every().wednesday.at("01:34").do(tasks.task_send_newsletter)
    schedule.every(2).minutes.do(tasks.task_send_reminder_email)
    schedule.every().wednesday.at("01:34").do(tasks.task_send_daily_report)
    while True:
        schedule.run_pending()
        
        time.sleep(1)

if __name__ == "__main__":
    try:
        run_scheduler()
        print('SCHEDULER STARTED')
    except KeyboardInterrupt:
        print("Scheduler oprit manual.")
        sys.exit()

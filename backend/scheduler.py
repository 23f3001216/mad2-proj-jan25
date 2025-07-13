import requests
from apscheduler.schedulers.background import BackgroundScheduler

scheduler_started = False

def start_scheduler(app):
    global scheduler_started
    if scheduler_started:
        print("Scheduler already started, skipping reinitialization.")
        return
    scheduler_started = True

    scheduler = BackgroundScheduler(timezone="Asia/Kolkata")

    def call_daily_reminder():
        with app.app_context():
            try:
                requests.get("http://localhost:5000/api/run-daily-reminder")
            except Exception as e:
                print("Daily Reminder API failed:", e)

    def call_monthly_report():
        with app.app_context():
            try:
                requests.get("http://localhost:5000/api/run-monthly-report")
            except Exception as e:
                print("Monthly Report API failed:", e)

    scheduler.add_job(call_daily_reminder, 'cron', hour=18, minute=59)
    scheduler.add_job(call_monthly_report, 'cron', day=13, hour=18, minute=59)

    scheduler.start()
    print("Scheduler started.")

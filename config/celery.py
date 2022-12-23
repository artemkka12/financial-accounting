import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config", result_backend="django-db")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request}")


app.conf.beat_schedule = {
    "deadline_today": {
        "task": "remind_deadline",
        "schedule": crontab(hour=6, minute=0),
        "args": (0,),
    },
    "deadline_tomorrow": {
        "task": "remind_deadline",
        "schedule": crontab(hour=6, minute=0),
        "args": (1,),
    },
    "deadline_in_a_week": {
        "task": "remind_deadline",
        "args": (7,),
        "schedule": crontab(hour=6, minute=0),
    },
    "monthly_report": {
        "task": "monthly_report",
        "schedule": crontab(hour=6, minute=0, day_of_month=1),
    },
}

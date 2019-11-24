"""
WSGI config for tj8890 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tj8890.settings")

application = get_wsgi_application()

from apscheduler.schedulers.background import BackgroundScheduler
from tj8890_item.views import check_dead_time


# 定时任务
scheduler = BackgroundScheduler()

# 每小时判断一次
scheduler.add_job(check_dead_time, 'cron', minute=0, second=0)

scheduler.start()

from celery.schedules import crontab
# app/core/celery_config.py

broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'UTC'
enable_utc = True


beat_schedule = {
    'generate-daily-inventory-report': {
        'task': 'app.services.celery_tasks.mail_summary.mail_daily_inventory_summary',
        # 'schedule': crontab(hour=22, minute=0),   #daily at 10 pm
        'schedule':60.0
    },
    'generate-weekly-po-report': {
        'task': 'app.services.celery_tasks.mail_summary.mail_weekly_po_summary',
        # 'schedule': crontab(hour=22, minute=0),   #daily at 10 pm
        'schedule':60.0
    }
}

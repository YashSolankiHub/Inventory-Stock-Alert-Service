from celery import Celery

celery_app = Celery(
    "celery_app",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)


celery_app.config_from_object('app.core.celery_config')

celery_app.autodiscover_tasks([
    'app.services.celery_tasks'
])


from app.services.celery_tasks import mail_summary
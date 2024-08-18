from celery import shared_task

from django.db import transaction
from django.db.models import F

from .models import RequestCounter


@shared_task
def update_request_counter():
    try:
        with transaction.atomic():
            request_counter, created = RequestCounter.objects.get_or_create(pk=1)
            request_counter.count = F('count') + 0.5
            request_counter.save()
    except Exception as e:
        print(f"Error updating request counter: {e}")
import logging

from celery import shared_task

from django.db import transaction
from django.db.models import F

from .models import RequestCounter

logger = logging.getLogger(__file__)

@shared_task
def update_request_counter():
    try:
        with transaction.atomic():
            request_counter, created = RequestCounter.objects.get_or_create(pk=1)
            logger.info(f'Updating Request Count')
            request_counter.count = F('count') + 1
            request_counter.save()
    except Exception as e:
        print(f"Error updating request counter: {e}")
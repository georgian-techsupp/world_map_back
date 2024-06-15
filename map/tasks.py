from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import Country

@shared_task
def delete_expired_countries():
    now = timezone.now()
    expired_countries = Country.objects.all()
    deleted_count = 0
    
    for country in expired_countries:
        expiry_days = country.expiry_days
        if expiry_days is not None:
            expiry_time = timedelta(days=expiry_days)
            if country.created < now - expiry_time:
                country.delete()
                deleted_count += 1
    
    return deleted_count
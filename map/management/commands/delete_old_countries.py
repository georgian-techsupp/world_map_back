from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from map.models import Country

class Command(BaseCommand):
    help = 'Delete countries older than 30 days'

    def handle(self, *args, **kwargs):
        threshold_date = timezone.now() - timedelta(days=30)
        deleted, _ = Country.objects.filter(created__lt=threshold_date).delete()
        self.stdout.write(f"Deleted {deleted} old countries.")
from datetime import datetime, timedelta
from random import randrange

from django.core.management import BaseCommand

from ...models import Invoice


class Command(BaseCommand):
    def handle(self, *args, **options):
        invoices = []
        for i in range(15):
            meter_start = randrange(1200000, 1300000)
            meter_start_time = datetime.now()
            invoices.append(Invoice(
                meterStart=meter_start,
                timestampStart=meter_start_time,
                meterStop=meter_start + randrange(1000, 100000),
                timestampStop=meter_start_time + timedelta(hours=randrange(0, 2), minutes=randrange(0, 59),
                                                           seconds=randrange(0, 59), ),
                energy=0.3,
                time=2,
                transaction=1,
            ))
        Invoice.objects.all().delete()
        Invoice.objects.bulk_create(invoices)

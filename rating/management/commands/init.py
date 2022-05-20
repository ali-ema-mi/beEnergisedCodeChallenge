from datetime import datetime, timedelta
from random import randrange

from django.core.management import BaseCommand

from ...models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        init_configurations()
        init_cdr()


def init_configurations():
    configurations = Configurations.instance()
    configurations.energy_fee = 0.3
    configurations.time_fee = 2
    configurations.transaction_fee = 1
    configurations.time_format = "%Y-%m-%dT%H:%M:%SZ"
    configurations.save()


def init_cdr():
    cdrs = []
    for i in range(15):
        meter_start = randrange(1200000, 1300000)
        meter_start_time = datetime.now()
        cdrs.append(CDR(
            meterStart=meter_start,
            meterStartTime=meter_start_time,
            meterStop=meter_start + randrange(1000, 100000),
            meterStopTime=meter_start_time + timedelta(hours=randrange(0, 2), minutes=randrange(0, 59),
                                                       seconds=randrange(0, 59), ),
        ))
    CDR.objects.all().delete()
    CDR.objects.bulk_create(cdrs)

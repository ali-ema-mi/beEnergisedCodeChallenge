from datetime import datetime

from django.conf import settings
from django.test import TestCase

from .models import Invoice


class RatingTestCase(TestCase):
    def setUp(self):
        pass

    def test_rating_formula(self):
        cdr = Invoice.objects.create(**{
            'meterStart': 1204307,
            'timestampStart': datetime.strptime("2021-04-05T10:04:00Z", settings.TIME_FORMAT),
            'meterStop': 1215230,
            'timestampStop': datetime.strptime("2021-04-05T11:27:00Z", settings.TIME_FORMAT),
            'energy': 0.3,
            'time': 2,
            'transaction': 1,

        })
        self.assertEqual(cdr.price(), 7.04)

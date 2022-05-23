from datetime import datetime

from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from .models import Invoice


class RatingTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_pricing_formula(self):
        '''
        Tests pricing formula
        :return: Test result
        '''
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

    #
    def test_pricing_endpoint(self):
        '''
        Testing invoice endpoint
        :return: Test result
        '''
        data = {
            "rate": {"energy": 0.3, "time": 2, "transaction": 1},
            "cdr": {"meterStart": 1204307, "timestampStart": "2021-04-05T10:04:00Z", "meterStop": 1215230,
                    "timestampStop": "2021-04-05T11:27:00Z"},
        }
        response = self.client.post(reverse("cdr-list"), data=data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = response.content.decode()
        self.assertEqual(response, '{"overall":7.04,"components":{"energy":3.277,"time":2.767,"transaction":1.0}}')

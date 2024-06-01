import time
import random

from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from faker import Faker
from .models import Card


class CardTests(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.login(username="testuser", password="12345")

    def test_create_card(self):
        url = "/api/v1/cards/"
        data = {"title": "Test Card", "card_number": "1122334455667788", "ccv": 103}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["is_valid"], False)

    def test_speed(self):
        start_time = time.time()
        api_url = "/api/v1/cards/"
        faker = Faker()

        for _ in range(100):

            data = {
                "card_number": faker.credit_card_number("visa16"),
                "ccv": random.randint(100, 999),
            }

            response = self.client.post(api_url, data, format="json")
            print(response.data)
            self.assertEqual(response.status_code, 201)

        end_time = time.time()
        self.assertLess(end_time - start_time, 60)

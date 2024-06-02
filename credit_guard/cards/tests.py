import time
import random

from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from faker import Faker


class CardTests(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username="testuser", password="12345")

        cls.faker = Faker()

        cls.data_to_send = []

        for _ in range(100):
            data = {
                "card_number": cls.faker.credit_card_number("visa16"),
                "ccv": random.randint(100, 999),
            }
            cls.data_to_send.append(data)

    def setUp(self) -> None:
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

        for i in self.data_to_send:
            response = self.client.post(api_url, i, format="json")
            print(response.data)
            self.assertEqual(response.status_code, 201)

        end_time = time.time()
        print("100 request finished in: ", end_time - start_time, "seconds")
        self.assertLess(end_time - start_time, 5)

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from image_app.models import User, Interaction, Image
from image_app.serializers import InteractionSerializer


class ImageAppTestCase(APITestCase):
    def setUp(self):

        self.user = User.objects.create(mobile_number="1234567890", otp="123456")
        self.user_url = reverse("register")
        self.otp_verification_url = reverse("verify_otp")
        self.homepage_url = reverse("homepage")
        self.interaction_url = reverse("image_interaction")
        self.history_url = reverse("history")

        self.image1 = Image.objects.create(name="One", url="http://example.com/one.png")
        self.image2 = Image.objects.create(name="Two", url="http://example.com/two.png")

    def test_register_view(self):
        response = self.client.post(self.user_url, {"mobile_number": "1234567891"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(User.objects.filter(mobile_number="1234567891").count(), 1)

    def test_verify_otp_view(self):

        response = self.client.post(
            self.otp_verification_url,
            {"mobile_number": "1234567890", "otp": "123456", "name": "Test User"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertTrue(User.objects.get(mobile_number="1234567890").is_verified)

        response = self.client.post(
            self.otp_verification_url, {"mobile_number": "1234567890", "otp": "654321"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_homepage_view(self):
        response = self.client.get(self.homepage_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["images"]), 2)
        self.assertEqual(response.data["images"][0]["name"], "One")
        self.assertEqual(
            response.data["images"][1]["url"], "http://example.com/two.png"
        )

    def test_image_interaction_view(self):
        self.user.is_verified = True
        self.user.save()

        response = self.client.post(
            self.interaction_url,
            {"user_id": self.user.id, "image_name": "One", "action": "accepted"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["success"])
        self.assertEqual(Interaction.objects.filter(user=self.user).count(), 1)
        response = self.client.post(
            self.interaction_url,
            {"user_id": 9999, "image_name": "one", "action": "accepted"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_history_view(self):
        self.user.is_verified = True
        self.user.save()

        Interaction.objects.create(user=self.user, image_name="One", action="like")
        Interaction.objects.create(user=self.user, image_name="Two", action="dislike")

        response = self.client.get(self.history_url, {"user_id": self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["history"]), 2)

        response = self.client.get(self.history_url, {"user_id": 9999})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

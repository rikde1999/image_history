from django.db import models
from django.utils import timezone
from image_app.choicefields import ActionMode


class User(models.Model):
    mobile_number = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name if self.name else self.mobile_number


class Interaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_name = models.CharField(max_length=50)
    action = models.CharField(
        choices=ActionMode.choices,
        max_length=20,
        default=ActionMode.ACTIONMODE_ACCEPTED,
    )

    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.name} - {self.image_name} - {self.action}"


class Image(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=200)

    def __str__(self):
        return self.name

from django.db import models
from django.utils.translation import gettext_lazy as _


class ActionMode(models.TextChoices):
    ACTIONMODE_ACCEPTED = "accepted", _("accepted")
    ACTIONMODE_REJECTED = "rejected", _("rejected")
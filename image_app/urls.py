from django.urls import path
from image_app.views import (
    RegisterView,
    VerifyOTPView,
    HomepageView,
    ImageInteractionView,
    HistoryView,
)  # CompletionView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify_otp"),
    path("homepage/", HomepageView.as_view(), name="homepage"),
    path(
        "image-interaction/", ImageInteractionView.as_view(), name="image_interaction"
    ),
    path("history/", HistoryView.as_view(), name="history"),
    # path('completion/', CompletionView.as_view(), name='completion'),
]

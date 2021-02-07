from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.SignUp.as_view(), name="signup"),
    path("thank-you/", views.thankyou, name="thank-you"),
    path("contact/", views.user_contact, name="contact")
]

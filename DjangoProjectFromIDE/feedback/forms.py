from django import forms
from django.core.mail import send_mail

from djangopv35_v1 import settings
from feedback.models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['fullName', 'email', 'phone', 'message']

    def send_email(self):
        fullName = self.cleaned_data['fullName']
        email_from = self.cleaned_data['email']
        message = self.cleaned_data['message']
        phone = self.cleaned_data['phone']

        print(f"Sending email...\nFrom: {fullName} <{email_from}>\nPhone: {phone}\nMessage: {message}")
        print(f"Email settings: Host={settings.EMAIL_HOST}, User={settings.EMAIL_HOST_USER}")

        if settings.EMAIL_HOST and settings.EMAIL_HOST_USER:
            # Email to Admin
            admin_subject = f"New Feedback from {fullName}"
            admin_message = f"""
            You have received new feedback.
            From: {fullName} ({email_from})
            Phone: {phone}
            Message:
            {message}
            """
            send_mail(
                admin_subject,
                admin_message,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],  # Admin's email
                fail_silently=False,
            )

            # Email to User
            user_subject = "Thank you for your feedback!"
            user_message = f"""
            Hi {fullName},

            We have received your feedback and will get back to you shortly.

            Best regards,
            The Team
            """
            send_mail(
                user_subject,
                user_message,
                settings.EMAIL_HOST_USER,
                [email_from],  # User's email
                fail_silently=False,
            )

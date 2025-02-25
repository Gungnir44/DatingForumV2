from .models import Notification
#from messages.models import Message  # Assuming you have a Message model
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Message  # ✅ Correct import


@receiver(post_save, sender=Message)
def notify_user(sender, instance, created, **kwargs):
    if created:
        subject = "New Message Notification"
        message = f"You have received a new message from {instance.sender.username}.\n\nMessage: {instance.content}"
        recipient_email = instance.receiver.email  # Ensure the User model has an email field

        # Print notification in terminal
        print(f"New message from {instance.sender} to {instance.receiver}")

        # Send email notification
        send_mail(
            subject,
            message,
            "your-email@example.com",  # Replace with your sender email
            [recipient_email],
            fail_silently=True,  # Prevents crashing if email fails
        )

@receiver(post_save, sender=Message)
def new_message_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=f"New message from {instance.sender.username}!"
        )

        # Send email notification
        send_mail(
            subject="New Message Alert",
            message=f"You have a new message from {instance.sender.username}. Log in to check it.",
            from_email="noreply@datingforum.com",
            recipient_list=[instance.receiver.email],
            fail_silently=True
        )

@receiver(post_save, sender=Message)
def new_message_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=f"New message from {instance.sender.username}!"
        )

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class Message(models.Model):
    id = models.BigAutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='received_messages')
    body = models.TextField(null=False)
    subject = models.TextField(null=False)
    creation_date = models.DateTimeField(default=timezone.now, null=False)
    is_read = models.BooleanField(default=False, null=False)

    def read(self, to_save=True):
        self.is_read = True
        if to_save:
            self.save()
        return {
            "sender": self.sender.id,
            "receiver": self.receiver.id,
            "subject": self.subject,
            "body": self.body,
            "creation_date": self.creation_date
        }
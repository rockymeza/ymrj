from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class OutgoingMessage(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    twilio_id = models.CharField(max_length=34)
    to_number = PhoneNumberField()
    body = models.TextField()

    def __str__(self):
        return '{number} ({time}) - {message}'.format(
            number=self.to_number,
            time=self.created_at,
            message=self.body,
        )

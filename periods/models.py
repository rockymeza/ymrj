from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class PeriodQuerySet(models.QuerySet):
    def active(self):
        return self.filter(end_date=None)


class Period(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    phone_number = PhoneNumberField()
    start_date = models.DateField()
    end_date = models.DateField(null=True)

    objects = PeriodQuerySet.as_manager()

    def __str__(self):
        return '{start}-{end}'.format(
            start=self.start_date,
            end=self.end_date,
        )

    def finish(self, end_date):
        self.end_date = end_date
        self.save(update_fields=['end_date'])

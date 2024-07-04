import uuid
from django.db import models
from users.models import User


class Availability(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_date = models.DateField()
    # For one-time availability start_date=end_date
    end_date = models.DateField(null=True, blank=True)
    # For recurring breaks (0-6, 0=Monday, 6=Sunday)
    day = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['start_time']),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(
                end_date__gte=models.F('start_date')), name='avail_end_date_gte_start_date'),
        ]

    def __str__(self):
        return f"{self.pk}"

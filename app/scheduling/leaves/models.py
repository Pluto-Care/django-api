import uuid
from django.db import models
from users.models import User
from django.utils.timezone import now


class Leave(models.Model):
    reason = (
        ('vacation', 'Vacation'),
        ('sick', 'Sick'),
        ('personal', 'Personal'),
        ('other', 'Other')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now)

    class Meta:
        indexes = [
            models.Index(fields=['start_date']),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(
                end_date__gt=models.F('start_date')), name='vacation_end_date_gt_start_date'),
        ]

    def __str__(self):
        return f"{self.pk}"

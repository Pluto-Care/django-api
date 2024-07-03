import uuid
from django.db import models
from django.utils.timezone import now
from users.models import User


class Break(models.Model):
    reason = (
        ('lunch', 'Lunch'),
        ('meeting', 'Meeting'),
        ('training', 'Training'),
        ('other', 'Other'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_date = models.DateField()
    # For one-time break start_date=end_date
    end_date = models.DateField(null=True, blank=True)
    # For recurring breaks (0-6, 0=Monday, 6=Sunday)
    day = models.IntegerField(null=True, blank=True)
    reason = models.CharField(max_length=10, choices=reason, default='other')
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(default=now)

    class Meta:
        indexes = [
            models.Index(fields=['start_time']),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(
                end_time__gt=models.F('start_time')), name='break_end_time_gt_start_time'),
        ]

    def __str__(self):
        return f"{self.pk}"

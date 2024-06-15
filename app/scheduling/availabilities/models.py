import uuid
from django.db import models
from users.models import User


class Availability(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_date = models.DateField()
    end_date = models.DateField()
    weekdays = models.JSONField()
    recurring = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['start_time']),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(
                end_time__gt=models.F('start_time')), name='avail_end_time_gt_start_time'),
            models.CheckConstraint(check=models.Q(
                end_date__gt=models.F('start_date')), name='avail_end_date_gt_start_date'),
        ]

    def __str__(self):
        return f"{self.pk}"


class Leave(models.Model):
    reason = (
        ('vacation', 'Vacation'),
        ('sick', 'Sick'),
        ('personal', 'Personal'),
        ('other', 'Other')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    availability = models.ForeignKey(Availability, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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


class Break(models.Model):
    reason = (
        ('lunch', 'Lunch'),
        ('meeting', 'Meeting'),
        ('training', 'Training'),
        ('other', 'Other'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    availability = models.ForeignKey(Availability, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    reason = models.CharField(max_length=10, choices=reason, default='other')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['start_time']),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(
                end_time__gt=models.F('start_time')), name='break_end_time_gt_start_time'),
            models.CheckConstraint(check=models.Q(
                end_date__gt=models.F('start_date')), name='break_end_date_gt_start_date'),
        ]

    def __str__(self):
        return f"{self.pk}"

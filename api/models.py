from django.db import models
from django.utils.translation import gettext_lazy as _


class Photographer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.email})"


class Event(models.Model):
    event_name = models.CharField(max_length=255)
    event_date = models.DateField()
    photographers_required = models.PositiveIntegerField(
        help_text=_("Number of photographers needed for the event")
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.event_name} on {self.event_date}"


class Assignment(models.Model):
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='assignments'
    )
    photographer = models.ForeignKey(
        Photographer, on_delete=models.CASCADE, related_name='assignments'
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'photographer')
        ordering = ['-assigned_at']
        verbose_name = _("Assignment")
        verbose_name_plural = _("Assignments")

    def __str__(self):
        return f"{self.photographer} -> {self.event}"

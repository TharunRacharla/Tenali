from django.db import models

class Reminder(models.Model):
    reminder_text = models.CharField(max_length=255)
    reminder_time = models.DateTimeField()

    def __str__(self):
        return f"{self.reminder_text} at {self.reminder_time}"

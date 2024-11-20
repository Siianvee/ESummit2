from django.db import models
import uuid

class Registration(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    ticket_code = models.CharField(max_length=10, unique=True, blank=True)

    def save(self, *args, **kwargs):
        # Generate a unique ticket code if it doesn’t exist
        if not self.ticket_code:
            self.ticket_code = str(uuid.uuid4())[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.email})"

class Sponsor(models.Model):
    name = models.CharField(max_length=100)
    logo_url = models.URLField()

    def __str__(self):
        return self.name

class Partner(models.Model):
    name = models.CharField(max_length=100)
    logo_url = models.URLField()

    def __str__(self):
        return self.name

class PanelDiscussion(models.Model):
    topic = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.topic

class Panelist(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    photo_url = models.URLField()
    panel = models.ForeignKey(PanelDiscussion, on_delete=models.CASCADE, related_name="panelists")

    def __str__(self):
        return f"{self.name} - {self.position}"

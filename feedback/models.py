from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

import misaka

from projects.models import Project

from django.contrib.auth import get_user_model
User = get_user_model()


class Feedback(models.Model):
    user = models.ForeignKey(User, related_name="feedback")
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    project = models.ForeignKey(Project, related_name="feedback",null=True, blank=True) #Every feedback belongs to a group there ForeignKey

    def __str__(self):
        return self.message

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        super().save(*args, **kwargs) #TODO Need to research what this function does

    def get_absolute_url(self):
        return reverse(
            "feedback:single",
            kwargs={
                "username": self.user.username,
                "pk": self.pk
            }
        )

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["user", "message"]

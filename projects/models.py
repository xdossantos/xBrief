from django.db import models
from django.utils.text import slugify #This will lowercase and add dashes to ulr slug
from django.core.urlresolvers import reverse
# Create your models here.

import misaka

from django.contrib.auth import get_user_model

User = get_user_model()

from django import template
register = template.Library() # This is how we can use custom template tags in the futre

class Project(models.Model): # I have replaced Group with Project
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    members = models.ManyToManyField(User,through="ProjectMember")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self): #have replaced groups with projects below
        return reverse("projects:single", kwargs={"slug": self.slug})

    class Meta:
        ordering = ["name"]

class ProjectMember(models.Model):
    project = models.ForeignKey(Project, related_name='memberships')
    user = models.ForeignKey(User, related_name='user_projects')

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together = ('project', 'user')

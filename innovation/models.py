from django.contrib.auth.models import User
from taggit.managers import TaggableManager
import settings
from django.db import models
from profiles.models import Profile

from .profile_extensions import InnovationProfile

#plugins needed for comments and tagging

class Evidence(models.Model):
    """
    Items can have links to evidence about how well they work. e.g. academic
    papers
    """
    title = models.CharField(max_length = 150, null = False, blank = False)
    url = models.URLField(null = False, blank = False)

    def __unicode__(self):
        return self.title


class Item(models.Model):
    """
    Instances of this class represent a specific innovation to be disseminated
    via our portal.  [these must have tags, comments]
    """
    title = models.CharField(max_length = 150, null = False, blank = False)
    created_on = models.DateTimeField(auto_now_add = True)
    created_by =  models.ForeignKey(User)
    evidence =  models.ManyToManyField(Evidence)
    description = models.TextField()
    tags = TaggableManager()

    class Meta:
        ordering = ['-created_on']

    def __unicode__(self):
        return self.title


class Specialisation(models.Model):
    """
    Items belong to a specialisation, e.g. Neurology or Immunology
    """
    name = models.CharField(max_length = 150, null = False, blank = False)
    item =  models.ForeignKey(Item)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class Vote(models.Model):
    """
    Users can vote against Items and Comments. Votes can only be positive.
    Votes must record the user Role and ID.
    """
    TARGET_TYPES = (
        ('item', 'Item'),
        ('comment', 'Comment'),
    )
    target_id = models.IntegerField(null = False, blank = False)
    target_type = models.CharField(max_length = 150, null = False,
        blank = False, choices=TARGET_TYPES)
    created_on = models.DateTimeField(auto_now_add = True)
    created_by =  models.ForeignKey(User)

    class Meta:
        ordering = ['-created_on']
        unique_together = ("target_id", "target_type")


Profile.register_extensions(InnovationProfile())

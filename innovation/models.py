from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.db import models
from profiles.models import Profile

from .profile_extensions import InnovationProfile

#plugins needed for comments and tagging

class Item(models.Model):
    """
    Instances of this class represent a specific innovation to be disseminated
    via our portal.  [these must have tags, comments]
    """
    title = models.CharField(max_length = 150, null = False, blank = False)
    slug = models.CharField(max_length = 150, null = False, unique = False)
    created_on = models.DateTimeField(auto_now_add = True)
    created_by = models.ForeignKey(User)
    summary = models.TextField()
    how_used = models.TextField()
    benefits = models.TextField()
    further_information = models.TextField()
    tags = TaggableManager()

    class Meta:
        ordering = ['-created_on']

    def __unicode__(self):
        return self.title


class Role(models.Model):
    name = models.CharField(max_length=255)

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

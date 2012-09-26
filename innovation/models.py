from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.db import models
from profiles.models import Profile

from .profile_extensions import InnovationProfile

from filebrowser.fields import FileBrowseField

#plugins needed for comments and tagging

class Item(models.Model):
    """
    Instances of this class represent a specific innovation to be disseminated
    via our portal.  [these must have tags, comments]
    """
    title = models.CharField(max_length = 150, null = False, blank = False)
    slug = models.CharField(max_length = 150, null = False, unique = True)
    created_on = models.DateTimeField(auto_now_add = True)
    created_by = models.ForeignKey(User)
    summary = models.TextField()
    how_used = models.TextField()
    benefits = models.TextField()
    further_information = models.TextField()
    tags = TaggableManager()
    hero_image = FileBrowseField(max_length=200, format='image',
                                                    blank=True, null=True,)

    class Meta:
        ordering = ['-created_on']

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('idea', (), {
        'slug': self.slug
        })

    @models.permalink
    def get_edit_url(self):
        return ('edit_idea', (), {
            'slug' : self.slug,
        })


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
        unique_together = ("target_id", "target_type", "created_by")


Profile.register_extensions(InnovationProfile())

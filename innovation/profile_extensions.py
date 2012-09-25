from django.db import models

def _name(self):
    return self.get_full_name() or self.username


class InnovationProfile(object):
    """ Profile extensions for Innovation project """

    def register(self, cls, admin_cls):
        # fields
        cls.add_to_class('role', models.ForeignKey('innovation.Role'))
        cls.add_to_class('patient_karma', models.IntegerField(null=True, blank=True))
        cls.add_to_class('clinician_karma', models.IntegerField(null=True, blank=True))
        cls.add_to_class('industry_karma', models.IntegerField(null=True, blank=True))
        cls.add_to_class('affiliation', models.CharField(max_length=255))
        cls.add_to_class('phone_number', models.CharField(max_length=50, null=True, blank=True))
        cls.add_to_class('bio', models.TextField(null=True, blank=True))
        cls.add_to_class('website', models.TextField(null=True, blank=True))

        cls.add_to_class('name', property(_name))

        cls.__unicode__ = cls.get_full_name

        # admin
        admin_cls.list_display_filter += ['role']

        admin_cls.fieldsets[0][1]['fields'].insert(3, 'affiliation')
        admin_cls.fieldsets[0][1]['fields'].insert(4, 'role')
        admin_cls.fieldsets[0][1]['fields'].insert(5, 'phone_number')
        admin_cls.fieldsets[1][1]['fields'].insert(3, 'bio')
        admin_cls.fieldsets[1][1]['fields'].insert(4, 'website')
        admin_cls.fieldsets.append(('Karma', {
            'fields': ['patient_karma', 'clinician_karma', 'industry_karma'],
            'classes': ['collapse'],
        }))


from django.db import models


class InnovationProfile(object):
    """ Profile extensions for Innovation project

    """
    def register(self, cls, admin_cls):
        # fields
        # cls.add_to_class('role', models.ForeignKey('innovation.Role'))
        cls.add_to_class('pseudonym', models.CharField(max_length=255))
        cls.add_to_class('is_pseudonymous', models.BooleanField(help_text='Use Pseudonym for comments and voting.'))
        cls.add_to_class('patient_karma', models.IntegerField())
        cls.add_to_class('clinician_karma', models.IntegerField())
        cls.add_to_class('industry_karma', models.IntegerField())
        cls.add_to_class('affiliation', models.CharField(max_length=255))

        cls.__unicode__ = cls.get_full_name

        # admin
        # admin_cls.list_display_filter += ['role']

        admin_cls.fieldsets[0][1]['fields'].insert(3, 'pseudonym')
        admin_cls.fieldsets[0][1]['fields'].insert(4, 'affiliation')
        admin_cls.fieldsets[1][1]['fields'].insert(1, 'is_pseudonymous')
        admin_cls.fieldsets.append(('Karma', {
            'fields': ['patient_karma', 'clinician_karma', 'industry_karma'],
            'classes': ['collapse'],
        }))


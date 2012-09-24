from profiles.models import Profile

from .profile_extensions import InnovationProfile


Profile.register_extensions(InnovationProfile())


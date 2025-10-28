import contextlib

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "tesys_tagboard.users"
    verbose_name = _("Users")

    def ready(self):
        with contextlib.suppress(ImportError):
            import tesys_tagboard.users.signals  # noqa: F401, PLC0415

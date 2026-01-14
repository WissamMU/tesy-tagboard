from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .enums import RatingLevel
from .enums import SupportedMediaTypes

validate_md5 = validators.RegexValidator(r"^[0-9A-Z]{32}$")
validate_phash = validators.RegexValidator(r"^[0-9a-z]{16}$")
validate_dhash = validators.RegexValidator(r"^[0-9a-z]{16}$")
validate_tag_name = validators.RegexValidator(r"^[a-z\d\:-_\s]+$")
validate_tagset_name = validators.RegexValidator(r"^[a-z\d\-_]+$")


def validate_tagset(tag_ids: list):
    msg = _("A tagset may only contain positive integers")
    try:
        for tag_id in tag_ids:
            if int(tag_id) < 0:
                raise ValidationError(msg)

    except (ValueError, TypeError) as e:
        raise ValidationError(msg) from e


def validate_media_file_is_supported(file):
    if not SupportedMediaTypes.find(file.content_type):
        msg = f"File with a content type of {file.content_type} is not supported"
        raise ValidationError(msg)


def validate_media_file_type_matches_ext(file):
    # TODO
    return


def validate_rating_level(value):
    levels = [x.value for x in RatingLevel]
    if value not in levels:
        msg = f"Rating levels must be one of {levels}"
        raise ValidationError(msg)

from dataclasses import dataclass
from enum import Enum

from django.utils.deconstruct import deconstructible


@dataclass
@deconstructible
class TagCategoryData:
    """Class for categorizes tags"""

    shortcode: str
    prefixes: set[str]
    display_name: str

    def __repr__(self):
        return f"<TagCategory: {self.shortcode} - {','.join(self.prefixes)}>"

    def __eq__(self, other):
        return (
            self.shortcode == other.shortcode
            and self.prefixes == other.prefixes
            and self.display_name == other.display_name
        )

    def __hash__(self):
        return hash(self.shortcode)


class TagCategory(Enum):
    """A basic tag with no prefix"""

    BASIC = TagCategoryData("BA", {"", "basic"}, "basic")
    ARTIST = TagCategoryData("AR", {"art", "artist"}, "artist")
    COPYRIGHT = TagCategoryData("CO", {"copy", "copyright"}, "copyright")

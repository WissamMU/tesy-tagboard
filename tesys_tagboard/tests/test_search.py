import pytest

from tesys_tagboard.enums import TagCategory
from tesys_tagboard.models import Tag
from tesys_tagboard.models import TagAlias
from tesys_tagboard.search import tag_alias_autocomplete
from tesys_tagboard.search import tag_autocomplete


# Arrange
@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        Tag.objects.bulk_create(
            [
                Tag(name="alabaster", category=TagCategory.BASIC.value.shortcode),
                Tag(name="amaranth pink", category=TagCategory.BASIC.value.shortcode),
                Tag(name="amaranth purple", category=TagCategory.BASIC.value.shortcode),
                Tag(name="amaranth", category=TagCategory.BASIC.value.shortcode),
                Tag(name="amber", category=TagCategory.BASIC.value.shortcode),
                Tag(name="arctic white", category=TagCategory.BASIC.value.shortcode),
                Tag(name="beige", category=TagCategory.BASIC.value.shortcode),
                Tag(name="black", category=TagCategory.BASIC.value.shortcode),
                Tag(name="blue jeans", category=TagCategory.BASIC.value.shortcode),
                Tag(name="blue", category=TagCategory.BASIC.value.shortcode),
                Tag(name="blue-gray", category=TagCategory.BASIC.value.shortcode),
                Tag(name="blueberry", category=TagCategory.BASIC.value.shortcode),
                Tag(name="brown", category=TagCategory.BASIC.value.shortcode),
                Tag(name="crimson", category=TagCategory.BASIC.value.shortcode),
                Tag(name="evergreen", category=TagCategory.BASIC.value.shortcode),
                Tag(name="green", category=TagCategory.BASIC.value.shortcode),
                Tag(name="grey", category=TagCategory.BASIC.value.shortcode),
                Tag(name="indigo", category=TagCategory.BASIC.value.shortcode),
                Tag(name="lime green", category=TagCategory.BASIC.value.shortcode),
                Tag(name="orange", category=TagCategory.BASIC.value.shortcode),
                Tag(name="purple", category=TagCategory.BASIC.value.shortcode),
                Tag(name="red", category=TagCategory.BASIC.value.shortcode),
                Tag(name="red vs. blue", category=TagCategory.BASIC.value.shortcode),
                Tag(name="sky blue", category=TagCategory.BASIC.value.shortcode),
                Tag(name="violet", category=TagCategory.BASIC.value.shortcode),
                Tag(name="violet hyacinth", category=TagCategory.BASIC.value.shortcode),
                Tag(name="white", category=TagCategory.BASIC.value.shortcode),
                Tag(name="white rapids", category=TagCategory.BASIC.value.shortcode),
                Tag(name="yellow", category=TagCategory.BASIC.value.shortcode),
                Tag(name="yellow flowers", category=TagCategory.BASIC.value.shortcode),
                Tag(
                    name="Avery Luis Stein", category=TagCategory.ARTIST.value.shortcode
                ),
                Tag(name="Elif", category=TagCategory.ARTIST.value.shortcode),
                Tag(name="Garbold Loop", category=TagCategory.ARTIST.value.shortcode),
                Tag(name="Justin Knope", category=TagCategory.ARTIST.value.shortcode),
                Tag(name="Solomon Steven", category=TagCategory.ARTIST.value.shortcode),
                Tag(name="Terry Toller", category=TagCategory.ARTIST.value.shortcode),
                Tag(name="Warren Witt", category=TagCategory.ARTIST.value.shortcode),
                Tag(name="Yura Yebolsky", category=TagCategory.ARTIST.value.shortcode),
                Tag(name="Zammy Zolan", category=TagCategory.ARTIST.value.shortcode),
                Tag(name="CC-BY", category=TagCategory.COPYRIGHT.value.shortcode),
                Tag(name="MIT", category=TagCategory.COPYRIGHT.value.shortcode),
                Tag(
                    name="Public Domain", category=TagCategory.COPYRIGHT.value.shortcode
                ),
                Tag(name="Unlicense", category=TagCategory.COPYRIGHT.value.shortcode),
            ]
        )

        TagAlias.objects.bulk_create(
            [
                TagAlias(name="arctic", tag=Tag.objects.get(name="arctic white")),
                TagAlias(name="gray", tag=Tag.objects.get(name="grey")),
                TagAlias(name="r v. b", tag=Tag.objects.get(name="red vs. blue")),
                TagAlias(name="r vs. b", tag=Tag.objects.get(name="red vs. blue")),
                TagAlias(name="red v. blue", tag=Tag.objects.get(name="red vs. blue")),
                TagAlias(name="red vs blue", tag=Tag.objects.get(name="red vs. blue")),
                TagAlias(name="red x blue", tag=Tag.objects.get(name="red vs. blue")),
                TagAlias(name="blue-berry", tag=Tag.objects.get(name="blueberry")),
                TagAlias(name="gray-blue", tag=Tag.objects.get(name="blue-gray")),
                TagAlias(name="bluejeans", tag=Tag.objects.get(name="blue jeans")),
                TagAlias(name="Justin K", tag=Tag.objects.get(name="Justin Knope")),
                TagAlias(name="Solomon S", tag=Tag.objects.get(name="Solomon Steven")),
                TagAlias(name="Z. Zolan", tag=Tag.objects.get(name="Zammy Zolan")),
            ]
        )


@pytest.mark.django_db
class TestTagAutocomplete:
    def test_autocomplete_included_by_name_partial(self, db):
        tags = tag_autocomplete(Tag.objects.all(), "blue")
        tag_names = [tag.name for tag in tags]
        assert "blue jeans" in tag_names
        assert "blue" in tag_names
        assert "blue-gray" in tag_names
        assert "blueberry" in tag_names
        assert "red vs. blue" in tag_names
        assert "sky blue" in tag_names
        assert tags.count() == 6

    def test_autocomplete_excluded_by_name_partial(self, db):
        tags = tag_autocomplete(Tag.objects.all(), exclude_partial="blue")
        tag_names = [tag.name for tag in tags]
        assert "blue jeans" not in tag_names
        assert "blue" not in tag_names
        assert "blue-gray" not in tag_names
        assert "blueberry" not in tag_names
        assert "sky blue" not in tag_names

    def test_autocomplete_excluded_by_tag_name(self, db):
        tags = tag_autocomplete(
            Tag.objects.all(), exclude_tag_names=["violet", "white", "yellow"]
        )
        tag_names = [tag.name for tag in tags]
        assert "violet" not in tag_names
        assert "white" not in tag_names
        assert "yellow" not in tag_names
        assert "white rapids" in tag_names
        assert "yellow flowers" in tag_names
        assert "violet hyacinth" in tag_names

    def test_autocomplete_excluded_by_tag(self, db):
        exclude_tags = Tag.objects.filter(
            category=TagCategory.COPYRIGHT.value.shortcode
        )
        tags = tag_autocomplete(Tag.objects.all(), exclude_tags=exclude_tags)
        assert len(tags.intersection(exclude_tags)) == 0


@pytest.mark.django_db
class TestTagAliasAutocomplete:
    def test_autocomplete_included_by_name_partial(self, db):
        aliases = tag_alias_autocomplete(TagAlias.objects.all(), "blue")
        alias_names = [alias.name for alias in aliases]
        assert "bluejeans" in alias_names
        assert "gray-blue" in alias_names
        assert "blue-berry" in alias_names
        assert "red v. blue" in alias_names
        assert "red vs blue" in alias_names
        assert "red x blue" in alias_names
        assert aliases.count() == 6

    def test_autocomplete_excluded_by_name_partial(self, db):
        aliases = tag_alias_autocomplete(TagAlias.objects.all(), exclude_partial="red")
        alias_names = [alias.name for alias in aliases]
        assert "red v. blue" not in alias_names
        assert "red vs blue" not in alias_names
        assert "red x blue" not in alias_names
        assert "r v. b" in alias_names
        assert "r vs. b" in alias_names

    def test_autocomplete_excluded_by_alias_name(self, db):
        aliases = tag_alias_autocomplete(
            TagAlias.objects.all(),
            exclude_alias_names=["Justin K", "Solomon S", "Z. Zolan"],
        )
        alias_names = [alias.name for alias in aliases]
        assert "Justin K" not in alias_names
        assert "Solomon S" not in alias_names
        assert "Z. Zolan" not in alias_names

    def test_autocomplete_excluded_by_alias(self, db):
        exclude_aliases = TagAlias.objects.filter(
            tag__category=TagCategory.COPYRIGHT.value.shortcode
        )
        aliases = tag_alias_autocomplete(
            TagAlias.objects.all(), exclude_aliases=exclude_aliases
        )
        assert len(aliases.intersection(exclude_aliases)) == 0

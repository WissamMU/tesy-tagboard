from ninja import NinjaAPI
from ninja import Schema
from ninja.orm import create_schema

from .enums import TagCategory
from .models import Tag

api = NinjaAPI()

TagSchema = create_schema(Tag)


class TagIn(Schema):
    name: str
    category_name: str | None = None
    rating_level: int


@api.get("/up")
def hello(request):
    return "This tagboard is up and running :)"


@api.get("/tags", response=list[TagSchema])
def get_tags(request):
    return Tag.objects.all()


@api.post("/tags")
def create_tag(request, params: TagIn):
    """
    Create a tag. Please provide:
    - **tag name**
    - **tag category** name
    - and **tag rating level** (defaults to 0)
    """

    if params.category_name is None:
        category = TagCategory.BASIC
    else:
        category = TagCategory.__members__.get(params.category_name.upper())
        if category is None:
            return {"error": "That tag category doesn't exist"}

    tag = Tag.objects.create(
        name=params.name,
        category=category.value.shortcode,
        rating_level=params.rating_level,
    )
    return {"id": tag.pk}

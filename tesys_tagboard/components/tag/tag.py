from dataclasses import dataclass

from django_components import Component
from django_components import register


@dataclass
class Action:
    name: str
    desc: str
    code: str


@register("tag")
class TagComponent(Component):
    template_file = "tag.html"
    js_file = "tag.js"

    def get_template_data(self, args, kwargs, slots, context):
        tag = kwargs.get("tag")
        category = tag.get_category_display()
        extra_actions = kwargs.get("actions", [])
        actions = [
            Action("search", "Search for posts with this tag", ""),
            Action("favorite", "Add this tag to your favorites", ""),
            Action("blocklist", "Add this tag to your tag blocklist", ""),
            *extra_actions,
        ]
        return {"tag": tag, "category": category, "actions": actions}

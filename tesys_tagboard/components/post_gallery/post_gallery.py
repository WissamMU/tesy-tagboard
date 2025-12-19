from django_components import Component
from django_components import register

from tesys_tagboard.models import Collection
from tesys_tagboard.models import CollectionQuerySet
from tesys_tagboard.models import PostQuerySet


@register("post_gallery")
class PostGalleryComponent(Component):
    template_file = "post_gallery.html"
    js_file = "post_gallery.js"

    def get_template_data(self, args, kwargs, slots, context):
        posts: PostQuerySet = kwargs.get("posts")
        collections: CollectionQuerySet = kwargs.get("collections", [])
        if self.request.user.is_authenticated:
            if collections:
                collections = collections.for_user(
                    self.request.user
                ).with_gallery_data()
            else:
                collections = Collection.objects.for_user(
                    self.request.user
                ).with_gallery_data()

        return {"collections": collections, "posts": posts}

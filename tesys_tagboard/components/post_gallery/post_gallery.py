from django_components import Component
from django_components import register

from tesys_tagboard.models import Collection
from tesys_tagboard.models import CollectionQuerySet


@register("post_gallery")
class PostGalleryComponent(Component):
    template_file = "post_gallery.html"
    js_file = "post_gallery.js"

    def get_template_data(self, args, kwargs, slots, context):
        pager = kwargs.get("pager")
        collections: CollectionQuerySet = kwargs.get("collections", [])

        # Must specificity an querystring arg name to render multiple
        # galleries on a single page
        query_page_arg_name = kwargs.get("query_page_arg_name", "page")
        page = kwargs.get("page")
        page_range = kwargs.get("page_range")

        # Authenticated users can use favorites and collection features
        if self.request.user.is_authenticated:
            if collections:
                collections = collections.for_user(
                    self.request.user
                ).with_gallery_data()
            else:
                collections = Collection.objects.for_user(
                    self.request.user
                ).with_gallery_data()

        return {
            "collections": collections,
            "query_page_arg_name": query_page_arg_name,
            "pager": pager,
            "page": page,
            "page_range": page_range,
        }

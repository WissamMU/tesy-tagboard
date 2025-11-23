from typing import TYPE_CHECKING
from typing import Any

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpRequest
from django.http import HttpResponse
from django.http.response import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_http_methods
from django.views.decorators.http import require_POST

from .enums import SupportedMediaTypes
from .enums import TagCategory
from .forms import PostForm
from .forms import PostSearchForm
from .models import Collection
from .models import Favorite
from .models import Image
from .models import Media
from .models import Post
from .models import Tag
from .search import PostSearch
from .search import tag_autocomplete

if TYPE_CHECKING:
    from django.core.files.uploadedfile import UploadedFile
    from django.db.models import QuerySet
    from django_htmx.middleware import HtmxDetails


class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


def home(request: HttpRequest) -> TemplateResponse:
    context = {}
    return TemplateResponse(request, "pages/home.html", context)


def post(request: HtmxHttpRequest, media_id: int) -> TemplateResponse:
    post = get_object_or_404(Post.objects.filter(media__id=media_id))
    context = {"post": post, "tags": Tag.objects.filter(post=post)}
    return TemplateResponse(request, "pages/post.html", context)


def posts(request: HtmxHttpRequest) -> TemplateResponse:
    data: dict[str, str | list[Any] | None] = {
        key: request.POST.get(key) for key in request.POST
    }
    data["tagset"] = request.POST.getlist("tagset")
    form = PostSearchForm(data) if request.method == "POST" else PostForm()

    posts = (
        Post.objects.all()
        .select_related("media", "media__image")
        .prefetch_related("tags")
        .all()
    )
    tags: QuerySet[Tag] | None = None
    if form.is_valid():
        tagset = form.cleaned_data.get("tagset")
        tags = Tag.objects.filter(pk__in=tagset)
        posts = posts.filter(tags__in=tags)

    # Get Posts favorited status
    favorites = Favorite.objects.filter(user=request.user)
    posts = Post.annotate_favorites(posts, favorites)

    pager = Paginator(posts, 20, 5)
    page_num = request.GET.get("page", 1)
    page = pager.get_page(page_num)
    context = {"posts": posts, "pager": pager, "page": page, "tags": tags}
    return TemplateResponse(request, "pages/posts.html", context)


def tags(request: HtmxHttpRequest) -> TemplateResponse:
    categories = TagCategory.__members__.values()
    tag_name = request.GET.get("q", "")
    tags_by_cat = {
        cat: Tag.objects.filter(category=cat.value.shortcode, name__icontains=tag_name)
        for cat in categories
    }

    context = {"tags_by_cat": tags_by_cat, "tag_name": tag_name}
    if request.htmx:
        return TemplateResponse(request, "tags/tags_by_category.html", context)

    return TemplateResponse(request, "pages/tags.html", context)


@login_required
def collections(request: HttpRequest) -> TemplateResponse:
    collections = Collection.objects.filter(public=True)
    pager = Paginator(collections, 25, 5)
    page_num = request.GET.get("page", 1)
    page = pager.get_page(page_num)
    context = {
        "user": request.user,
        "collections": collections,
        "pager": pager,
        "page": page,
    }
    return TemplateResponse(request, "pages/collections.html", context)


@login_required
def collection(request: HtmxHttpRequest, collection_id: int) -> TemplateResponse:
    collection = get_object_or_404(Collection.objects.filter(pk=collection_id))
    posts = Post.objects.filter(pk__in=collection.posts.values_list("pk", flat=True))
    pager = Paginator(posts, 25, 5)
    page_num = request.GET.get("page", 1)
    page = pager.get_page(page_num)
    context = {
        "user": request.user,
        "collection": collection,
        "pager": pager,
        "page": page,
    }
    return TemplateResponse(request, "pages/collection.html", context)


@login_required
@require_http_methods(["PUT"])
def add_favorite(request: HtmxHttpRequest, post_id: int) -> HttpResponse:
    if request.htmx:
        try:
            post = Post.objects.get(pk=post_id)
            favorite = Favorite.objects.create(post=post, user=request.user)
            favorite.save()
            return render(
                request,
                "icons/feather.html",
                context={"icon": "heart", "fill": True},
                status=200,
            )
        except Post.DoesNotExist, Favorite.DoesNotExist:
            return HttpResponse(status=404)
    return HttpResponse("Not allowed", status=403)


@login_required
@require_http_methods(["DELETE"])
def remove_favorite(request: HtmxHttpRequest, post_id: int) -> HttpResponse:
    try:
        post = Post.objects.get(pk=post_id)
        Favorite.objects.get(post=post, user=request.user).delete()
        return render(
            request,
            "icons/feather.html",
            context={"icon": "heart", "fill": False},
            status=200,
        )
    except Post.DoesNotExist, Favorite.DoesNotExist:
        return HttpResponse(status=404)
    return HttpResponse("Not allowed", status=403)


@login_required
@require_http_methods(["POST"])
def add_post_to_collection(
    request: HtmxHttpRequest, collection_id: int
) -> HttpResponse:
    if request.htmx:
        try:
            collection = Collection.objects.get(user=request.user, pk=collection_id)
            post = Post.objects.get(pk=request.POST.get("post"))
            collection.posts.add(post)

            return render(
                request,
                "collections/picker_item.html",
                context={"collection": collection, "post": post, "checked": True},
                status=200,
            )
        except Post.DoesNotExist, Collection.DoesNotExist:
            return HttpResponse(status=404)
    return HttpResponse("Not allowed", status=403)


@login_required
@require_http_methods(["POST"])
def remove_post_from_collection(
    request: HtmxHttpRequest, collection_id: int
) -> HttpResponse:
    if request.htmx:
        try:
            collection = Collection.objects.get(user=request.user, pk=collection_id)
            post = Post.objects.get(pk=request.POST.get("post"))
            collection.posts.remove(post)

            return render(
                request,
                "collections/picker_item.html",
                context={"collection": collection, "post": post, "checked": False},
                status=200,
            )
        except Post.DoesNotExist, Collection.DoesNotExist:
            return HttpResponse(status=404)
    return HttpResponse("Not allowed", status=403)


@require_GET
def post_search_autocomplete(
    request: HtmxHttpRequest,
) -> TemplateResponse | HttpResponseNotAllowed:
    if request.method == "GET" and request.htmx:
        tag_prefixes = [key.lower() for key in TagCategory.__members__]
        query = request.GET.get("q", "")
        ps = PostSearch(query, tag_prefixes)
        partial = request.GET.get("partial", "")
        items = ps.autocomplete(partial)

        context = {"items": items}
        return TemplateResponse(request, "posts/search_autocomplete.html", context)

    return HttpResponseNotAllowed(["GET"])


@require_GET
def tag_search_autocomplete(
    request: HtmxHttpRequest,
) -> TemplateResponse | HttpResponseNotAllowed:
    if request.method == "GET":
        partial = request.GET.get("partial", "")
        tags = tag_autocomplete(partial)
        context = {"tags": tags}
        return TemplateResponse(request, "tags/search_autocomplete.html", context)

    return HttpResponseNotAllowed(["GET"])


def handle_media_upload(file: UploadedFile | None, src_url: str | None) -> Media:
    """Detects media type and creates a new Media derivative"""
    if file is None:
        msg = "A file must be provided to upload"
        raise ValueError(msg)

    if file.content_type:
        if smt := SupportedMediaTypes.find(file.content_type):
            media = Media(orig_name=file.name, type=smt.name, src_url=src_url)
            media.save()

            # TODO: match on media type (image, video, audio)...
            img = Image(file=file, meta=media)
            img.save()

            return media

        msg = "That file extension is not supported"
        raise ValueError(msg)

    msg = "Provided file doesn't have a content type"
    raise ValueError(msg)


@require_POST
def upload(request: HtmxHttpRequest) -> TemplateResponse:
    data: dict[str, str | list[Any] | None] = {
        key: request.POST.get(key) for key in request.POST
    }
    data["tagset"] = request.POST.getlist("tagset")
    form = PostForm(data, request.FILES) if request.method == "POST" else PostForm()

    if form.is_valid():
        media = handle_media_upload(
            form.cleaned_data.get("file"), form.cleaned_data.get("src_url")
        )

        tagset = form.cleaned_data.get("tagset")
        tags = Tag.objects.filter(pk__in=tagset)
        post = Post(uploader=request.user, media=media)
        post.tags.set(tags)
        post.save()

    context = {"form": form}
    return TemplateResponse(request, "pages/upload.html", context)


@require_GET
def search_help(request: HtmxHttpRequest) -> TemplateResponse:
    context = {}
    return TemplateResponse(request, "pages/help.html", context)

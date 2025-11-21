from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.db.models import QuerySet
from django.http import HttpRequest
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import RedirectView
from django.views.generic import UpdateView
from django_htmx.middleware import HtmxDetails

from tesys_tagboard.models import Collection
from tesys_tagboard.models import Favorite
from tesys_tagboard.users.models import User


class HtmxHttpRequest(HttpRequest):
    htmx: HtmxDetails


@login_required
def user_detail_view(request: HttpRequest, username: str) -> TemplateResponse:
    user = request.user
    favorites = Favorite.objects.filter(user=user)
    collections = Collection.objects.filter(user=user)

    favorites_pager = Paginator(favorites, 20, 5)
    favorites_page_num = request.GET.get("fav_page", 1)
    favorites_page = favorites_pager.get_page(favorites_page_num)

    context = {
        "user": user,
        "favorites_pager": favorites_pager,
        "favorites_page": favorites_page,
        "collections": collections,
    }
    return TemplateResponse(request, "users/user_detail.html", context)


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self) -> str:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user.get_absolute_url()

    def get_object(self, queryset: QuerySet | None = None) -> User:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self) -> str:
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()

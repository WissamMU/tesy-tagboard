from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Image
from .models import Tag
from .models import TagAlias


class UploadImage(forms.ModelForm):
    src_url = forms.URLField(label=_("Source"), required=False)

    class Meta:
        model = Image
        fields = ["file"]


class MakeTag(forms.Form):
    class Meta:
        model = Tag
        fields = ["name", "category"]


class MakeTagAlias(forms.ModelForm):
    class Meta:
        model = TagAlias
        fields = ["name", "tag"]


class TagSearch(forms.Form):
    pass


class PostForm(forms.Form):
    src_url = forms.URLField(label=_("Source"), required=False)
    file = forms.FileField(label="File", required=True)

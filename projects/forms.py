from dataclasses import field, fields
from django.forms import ModelForm, widgets
from django import forms
from .models import Mod, Review, Gallery
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ModForm(ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget(config_name="default"))

    class Meta:
        model = Mod
        fields = [
            "title",
            "featured_image",
            "short_intro",
            "description",
            "modfile",
            "tags",
        ]
        widgets = {
            "tags": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ModForm, self).__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "input",
                    "style": "background-color: var(--color-sub-light); color: var(--color-light);",
                }
            )


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ["value", "body"]
        labels = {"value": "Place u'r vote", "body": "Add a comment with u'r vote"}

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "input",
                    "style": "background-color: var(--color-sub-light); color: var(--color-light);",
                }
            )


class ImageForm(ModelForm):
    class Meta:
        model = Gallery
        fields = ["img", "title"]

    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": "input",
                    "style": "background-color: #1c19218f; color: var(--color-light);",
                }
            )

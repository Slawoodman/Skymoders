from dataclasses import field, fields
from django.forms import ModelForm, widgets
from django import forms
from .models import Mod, Review


class ModForm(ModelForm):
    class Meta:
        model = Mod
        fields = ['title', 'featured_image', 'description', 'download_link', 'tags']
        widgets  = {
            'tags': forms.CheckboxSelectMultiple(),
        }


    def __init__(self, *args, **kwargs):
        super(ModForm, self).__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']
        labels = {
            'value': "Place u'r vote",
            'body': "Add a comment with u'r vote"
        }
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})



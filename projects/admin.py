from django.contrib import admin
from .models import Gallery, Mod, Review, Tag

# Register your models here.

admin.site.register(Mod)
admin.site.register(Review)
admin.site.register(Tag)
admin.site.register(Gallery)

from modeltranslation.translator import register, TranslationOptions
from .models import (
    Comments,
    News, Category
)

@register(Category)
class CategoryTransOpt(TranslationOptions):
    fields = ("name", )


@register(News)
class CategoryTransOpt(TranslationOptions):
    fields = ("title", "subtitle", "post")


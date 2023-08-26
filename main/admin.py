import random
from django.contrib import admin
from .models import (
    Ads,
    News,
    Comments,
    Category,
    MainNews, BaseVariables,
    Contact, Social, Subscribes, SendedNews
)
from django.utils.safestring import mark_safe
# Register your models here.


admin.action(description="Clone")
def Clone(modeladmin, request, queryset):
    for news in queryset:
        news.pk = None
        news.slug = str(random.randint(9999, 999999999))
        news.save()


admin.action(description="Published") 
def Published(modeladmin, request, queryset):
    queryset.update(status='pub')


admin.action(description="Pending")
def Pendding(modeladmin, request, queryset):
    queryset.update(status='pen')


admin.action(description="Comment On")
def CommentOn(modeladmin, request, queryset):
    queryset.update(comment_on_off=True)


admin.action(description="Comment Off")
def CommentOff(modeladmin, request, queryset):
    queryset.update(comment_on_off=False)


admin.action(description="Favorites On")
def FavoriteOn(modeladmin, request, queryset):
    queryset.update(favorite=True)


admin.action(description="Favorites Off")
def FavoriteOff(modeladmin, request, queryset):
    queryset.update(favorite=False)


""" CATEGORY ADMIN """
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    actions = [Clone]
    ordering = ("order_num", )
    list_filter = ("add_time", )   
    list_editable = ("order_num", )
    list_display_links = ("name_uz", ) 
    prepopulated_fields = {"slug": ("name_uz", )}
    list_display = ("id", "name_uz", "author", "order_num",)
    search_fields = ("name_uz","name_uz_Cyrl", "name_ru", "name_en")
    fieldsets = (
        ("Tarjima bo'ladigan bo'limlar", {
            "fields": (
                "name_uz", 
                "name_uz_Cyrl",
                ("name_ru", "name_en"), 
            ),
        }),
        ("Umumiy bo'limlar", {
            "fields": (
                "order_num",
            ),
        }),
        ("Automatik to'ldiriladigan bo'limlar", {
            "classes": ("collapse", ),
            "fields": (
                "author",
                "slug",
            ),
        }),
    )

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        return super().save_model(request, obj, form, change)


""" NEWS MODEL ADMIN """
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    ordering = ("-add_time",)
    sortable_by = ["category"] 
    date_hierarchy = 'add_time'
    show_full_result_count = True
    readonly_fields = ("Preview", )
    list_display_links = ("title_uz", )
    list_editable = ("category", "uzbekiston_news", "favorite", "comment_on_off", "status")
    actions = [Clone, Published, Pendding, CommentOn, CommentOff, FavoriteOn, FavoriteOff]
    list_filter = ("add_time", "category", "status", "uzbekiston_news", "favorite", "comment_on_off", "breaking_news")
    list_display = ("id", "title_uz", "category", "add_time", "uzbekiston_news", "favorite", "comment_on_off", "status")
    search_fields = ("title_uz", "title_uz_Cyrl", "title_ru", "title_en", "subtitle", "subtitle_uz_Cyrl", "subtitle_ru", "subtitle_en")

    fieldsets = (
        ("Umumiy bo'limlar", {
            "fields": (
                "category",                                                     
                "status",                                                       
                "author_news",
                "add_time",
                ("post_img", "Preview"),                                                     
                ("post_video", "post_file"),    
                ("favorite", "comment_on_off", "breaking_news", "uzbekiston_news") 
            ),
        }),
        ("O'zbek tilida to'ldirish", {
            "fields": (
                "title_uz", "subtitle_uz", "post_uz"
            ),
        }),
        ("O'zbek (kiril yozuvida) tilida to'ldirish", {
            "classes": ("collapse", ),
            "fields": (
                "title_uz_Cyrl", "subtitle_uz_Cyrl", "post_uz_Cyrl"
            ),
        }),
        ("Rus tilida to'ldirish", {
            "classes": ("collapse", ),
            "fields": (
                "title_ru", "subtitle_ru", "post_ru"
            ),
        }),
        ("Ingiliz tilida to'ldirish", {
            "classes": ("collapse", ),
            "fields": (
                "title_en", "subtitle_en", "post_en"
            ),
        }),
        ("Automatik to'ldiriladigan bo'limlar", {
            "classes": ("collapse", ),
            "fields": (
                "author", "slug", "post_view", "comment_count", 
            ),
        }),
    )
    
    def Preview(self, obj):
        return mark_safe(f"<img src='{obj.post_img.url}' alt='{obj.title}' width='400'>")

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        return super().save_model(request, obj, form, change)

    def get_prepopulated_fields(self, request, obj):
        return {"slug": ('title_uz',)}


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    ordering = ("-add_time", )
    date_hierarchy = "add_time"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    list_filter = ("add_time", )
    list_display_links = ("f_name", )
    list_display = ("id", "f_name", "news", "add_time")


@admin.register(MainNews)
class MainNewsAdmin(admin.ModelAdmin):   
    ordering = ("order_num", ) 
    list_editable = ("order_num", )
    filter_horizontal = ("posts", )
    list_display_links = ("GetName", )
    list_filter = ("category", "add_time")
    list_display = ("id", "GetName", "NewsCount", "order_num", "add_time")

    def GetName(self, obj):
        return obj.category.name
    GetName.short_description = "Bo'lim nomi"


    def NewsCount(self, obj):
        total = obj.posts.all().count()
        return f"{total} ta"
    NewsCount.short_description = "Yangiliklar soni"
    

@admin.register(Ads)
class AdsAdmin(admin.ModelAdmin):
    ordering = ("-add_time", )
    search_fields = ("note", )
    date_hierarchy = "add_time"
    list_display_links = ("note", )
    actions = [Pendding, Published, Clone]
    list_editable = ("status", "location")
    list_filter = ("status", "location", "add_time")
    list_display = ("id", "note", "status", "location", "link", "add_time",)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    ordering = ["-add_time"]
    list_filter = ("add_time", )
    list_display_links = ("f_name", )
    list_display = ("id", "f_name", "email", "subject", "add_time")

 
@admin.register(Social)
class SocialAdmin(admin.ModelAdmin):
    ordering = ("order_num", )
    list_filter = ("add_time", )
    list_editable = ["order_num"]
    list_display_links = ("name", )
    list_display = ("id", "name", "order_num", "add_time")


@admin.register(Subscribes)
class SubscribeAdmin(admin.ModelAdmin):
    ordering = ("-add_time", )
    list_display_links = ("email", )
    list_filter = ("add_time", "status")
    list_display = ("id", "email", "status", "add_time")

    
@admin.register(BaseVariables)
class VariableAdmin(admin.ModelAdmin):
    list_editable = ("name", "theme", "email", "phone", "address") 
    list_display = ("id", "name", "theme", "email", "phone", "address")


@admin.register(SendedNews)
class SendedNewsAdmin(admin.ModelAdmin):
    list_display = ("id", "news", "add_time")
from django.db import models
from django.urls import reverse
from colorfield.fields import ColorField
from django_quill.fields import QuillField
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

Author = get_user_model()

# Create your models here.
class Category(models.Model):
    """ Categorialar uchun """
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=250, verbose_name=_("Categoriyalar"), help_text=_("Sport, Biznes, Dunyo ...vhk"), unique=True, null=True, blank=True)
    order_num = models.IntegerField(default=0, verbose_name=_("Tartib raqami"))
    slug = models.SlugField(unique=True, blank=True, null=True, verbose_name="Slug", help_text=_("Bu automatik to'ldiriladi"))
    add_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = ""
        managed = True
        verbose_name = _("Bo'limlar")
        verbose_name_plural = _("Bo'limlar")
    
    def __str__(self):
        return self.name

STATUS = (
    ("pub", "Published"),
    ("pen", "Pendding"),
)

class News(models.Model):
    """ Yangiliklar joylash uchun """
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=700, verbose_name=_("Yangilik sarlovhasi"), help_text=_("Matn uchunligi 700ta belgidan oshmasligi kerak"), null=True, blank=True)
    subtitle = models.CharField(max_length=1500, verbose_name=_("Yangilikning qisqacha mazmuni"), null=True, blank=True, help_text=_("Matn uzunligi 1500ta so'zdan oshmasligi kerak"))
    post = QuillField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    post_img = models.FileField(upload_to="yangiliklar/images/%Y-%M-%D/", null=True, blank=True, verbose_name=_("Asosiy rasm"), help_text=_("Rasmli fayllar uchun"))
    post_file = models.FileField(upload_to="yangiliklar/pdf-file/%Y-%M-%D/", null=True, blank=True, verbose_name=_("PDF faylar uchun"))
    post_video = models.FileField(upload_to="yangiliklar/videos/%Y-%M-%D/", null=True, blank=True, verbose_name=_("Video"), help_text=_("Video faylar uchun"))
    author_news = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=222, choices=STATUS, default="pub")
    favorite = models.BooleanField(default=False, verbose_name=_("Mualif tanlovi"))
    breaking_news = models.BooleanField(default=False, verbose_name=_("Teskor yangilik"))
    comment_on_off = models.BooleanField(default=False, verbose_name=_("Izoh"), help_text=_("Izohlarni ko'rsatish yoki o'chirib qo'yish"))
    uzbekiston_news = models.BooleanField(default=False)
    comment_count = models.IntegerField(default=0, help_text=_("Tegilmasin"))
    post_view = models.IntegerField(default=0, verbose_name=_("Yangilikni ko'rishlar soni"))
    slug = models.SlugField(unique=True, blank=True, null=True)
    update_time = models.DateTimeField(auto_now=True)
    add_time = models.DateTimeField(verbose_name=_("Yangilik sanasi"), null=True, blank=True)


    class Meta:
        db_table = ""
        managed = True
        verbose_name = _("Yangiliklar")
        verbose_name_plural = _("Yangiliklar")

    def get_absolute_url(self):
        return reverse("detail_news", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.category} | {self.title[:50]}"

    def set_html(self):
        html = self.post.html
        return html
        

class Comments(models.Model):
    """ IZOHLAR UCHUN """
    news = models.ForeignKey(News, on_delete=models.SET_NULL, null=True, blank=True)
    f_name = models.CharField(max_length=250, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.f_name)
    
    def get_absolute_url(self):
        return reverse("detail_news", kwargs={"slug": self.news.slug})


class MainNews(models.Model):
    """ TANLAB OLINADIGAN YANGILIKLAR """
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Bo'lim nomi"))
    posts = models.ManyToManyField(News, related_name="news", verbose_name=_("Yangiliklar"), help_text=_("Web saytda ko'rinishi kerak Bo'lgan yangiliklarni tanlang"))
    order_num = models.IntegerField(default=0, verbose_name=_("Tartib raqam"))
    add_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.category.name)


    class Meta:
        db_table = ""
        managed = True
        verbose_name = _("Asosiy Yangiliklar")
        verbose_name_plural = _("Asosiy Yangiliklar")


AD_LOCATION = (
    ("top", "Yuqori"),
    ("middle", "o'rta"),
    ("left", "Yon tomon"),
    ("bottom", "Pastki"),
)
class Ads(models.Model):
    """ Reklamalarni jo'ylashtirish """
    note = models.CharField(max_length=777, verbose_name=_("Eslatma"), help_text=_("Ozingiz uchun eslatma yozing reklama xaqida"))
    ads_video = models.FileField(upload_to="Ads/videos/%Y-%M-%D/", null=True, blank=True, verbose_name=_("Video fayl"), help_text=_("Videoli reklama uchun"))
    ads_image = models.ImageField(upload_to="Ads/images/%Y-%M-%D/", null=True, blank=True, verbose_name=_("Rasm"), help_text=_("Rasmli fayl uchun"))
    status = models.CharField(max_length=100, choices=STATUS, default="pub", verbose_name=_("Reklama statusi"), help_text=_("Published = Reklamani ko'rsatish, Pendding = Reklamani Ushlab turish"), null=True, blank=True)
    location = models.CharField(max_length=111, choices=AD_LOCATION, null=True, blank=True, verbose_name=_("Reklamani ko'rinish joyi"), help_text=_("Tanlash shart*"))
    link = models.URLField(null=True, blank=True, help_text=_("Web site yoki ijtimoi tarmoq linki"))
    add_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.note}"

    class Meta:
        db_table = ""
        managed = True
        verbose_name = _("Reklama")
        verbose_name_plural = _("Reklama")


class Contact(models.Model):
    """ XATLAR """
    f_name = models.CharField(
        max_length=100, 
        verbose_name=_("F.I.SH"), 
        help_text=_("Akmal Akmalov Akmalivich"), 
        error_messages={
            "null": _("F.I.SH ni kiritishingiz kerak."),
            "blank": _("F.I.SH ni kiritishingiz kerak."),
        }
    )
    email = models.EmailField(
        max_length=120, verbose_name=_("E-Pochta"),
        help_text=_("E-Pochta: admin@gmail.com"),
        error_messages={
            "invalid": _("Siz notog'ri pochta kiritingiz, \n Misol uchun: admin@example.com"),
            "null": _("E-Pochta ni kiritishingiz kerak."),
            "blank": _("E-Pochta ni kiritishingiz kerak."),
        }
    )
    subject = models.CharField(
        max_length=150, verbose_name=_("Xatning qisqacha mazmuni"),
        error_messages={
            "null": _("Mavzuni ni kiritishingiz kerak."),
            "blank": _("Mavzuni ni kiritishingiz kerak."),
        }
    )
    message = models.TextField(
        verbose_name=_("Xat"), 
        error_messages={
            "null": _("Xat mazmuni kiritishingiz kerak."),
            "blank": _("Xat mazmuni kiritishingiz kerak."),
        })
    add_time = models.DateTimeField(auto_now_add=True, verbose_name=_("Xat kelgan vaqt"))
    update_time = models.DateTimeField(auto_now=True, verbose_name=_("Xat o'qilgan vaqt"))

    def __str__(self):
        return f"{self.f_name}"


    class Meta:
        db_table = ""
        managed = True
        verbose_name = _("Xat")
        verbose_name_plural = _("Xatlar")


class Social(models.Model):
    """ IJTIMOIY TARMOQLAR """
    name = models.CharField(max_length=120, verbose_name="Nomi", null=True, blank=True)
    icon = models.CharField(max_length=120, verbose_name="Icon", null=True, blank=True)
    url = models.URLField(verbose_name="URL", null=True, blank=True)
    bg_color = ColorField(default="#123456")
    order_num = models.IntegerField(default=0)
    add_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.name}"
 

    class Meta:
        db_table = ""
        managed = True
        ordering = ["order_num"]
        verbose_name = _("Ijtimoiy tarmoqlar")
        verbose_name_plural = _("Ijtimoiy tarmoqlar")



class Subscribes(models.Model):
    """ SUBSCRIBE'S EMAIL """
    email = models.EmailField(
        verbose_name="Email", unique=True,
        error_messages={
            "unique": _("Bu email oldin ham ro'yhatdan o'tkan"),
            "null": _("E-pochta ni kiritishingiz kerak."),
            "blank": _("E-pochta ni kiritishingiz kerak."),
            "invalid": _("Bu xaqiqiy email emas."),
        }
    )
    status = models.BooleanField(default=True)
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.email}"
    
    
    class Meta:
        db_table = ''
        managed = True
        ordering = ["-add_time"]
        verbose_name = _("Obuna bo'lganlar")
        verbose_name_plural = _("Obuna bolganlar")


class BaseVariables(models.Model):
    """ UMUMIY OZGARUVCHILAR """
    theme = ColorField(verbose_name=_("veb sayt uchun asosiy rang"))
    logo = models.FileField(upload_to="logo/", null=True, blank=True)
    favilcon = models.FileField(upload_to="favilcon/", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=_("veb sayt nomi"))
    email = models.EmailField(max_length=250, verbose_name=_("Admin e-pochtasi"))
    phone = models.CharField(_("Admin telefon raqami"), max_length=50)
    address = models.CharField(_("Manzil"), max_length=150)
    add_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}" 

    class Meta:
        db_table = ''
        managed = True
        ordering = ("-add_time", )
        verbose_name = _("Umumiy ozgaruvchilar")
        verbose_name_plural = _("Umumiy ozgaruvchilar")
           

class SendedNews(models.Model):
    """ OBUNACHILARGA YETKAZILGAN YANGILIKLAR """
    news = models.OneToOneField(News, null=True, blank=True, unique=True, on_delete=models.SET_NULL)
    add_time = models.DateTimeField(auto_now_add=True)
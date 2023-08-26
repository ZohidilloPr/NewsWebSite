from .models import (
    News, Category, MainNews, Social, Ads, BaseVariables
)
from datetime import datetime
from .forms import FormWithCaptcha
from django.utils.translation import gettext_lazy as _

def common_variables(request):
    today = datetime.now()
    try:
        name = BaseVariables.objects.last().name
        logo = BaseVariables.objects.last().logo
        email = BaseVariables.objects.last().email
        theme = BaseVariables.objects.last().theme
        phone = BaseVariables.objects.last().phone
        address = BaseVariables.objects.last().address
        favilcon = BaseVariables.objects.last().favilcon
        social = Social.objects.all().order_by("order_num")
        main_news = MainNews.objects.all().order_by("order_num")
        categories = Category.objects.all().order_by("order_num")
        tree_news = News.objects.filter(status="pub").order_by("-add_time")[:4]
        last_news_two_1 = News.objects.filter(status="pub").order_by("-add_time")[4:6]
        last_news_two_2 = News.objects.filter(status="pub").order_by("-add_time")[6:8]
        last_news_two_5 = News.objects.filter(status="pub").order_by("-add_time")[8:9]
        last_news_two_6 = News.objects.filter(status="pub").order_by("-add_time")[9:13]
        ads_top = Ads.objects.filter(status="pub", location="top").order_by("-add_time")
        ads_left = Ads.objects.filter(status="pub", location="left").order_by("-add_time")
        the_most_viewest_news = News.objects.filter(status="pub").order_by("-post_view")[:4]
        ads_middle = Ads.objects.filter(status="pub", location="middle").order_by("-add_time")
        ads_bottom = Ads.objects.filter(status="pub", location="bottom").order_by("-add_time")
        the_most_commited_news = News.objects.filter(status="pub").order_by("-comment_count")[:4]
        favorite_news = News.objects.filter(favorite=True, status="pub").all().order_by("-add_time")[:8]
        uzbekistan_news = News.objects.filter(uzbekiston_news=True, status="pub",).order_by("-add_time")[:4]
        breaking_news = News.objects.filter(breaking_news=True, status="pub").all().order_by("-add_time")[:8]
    except Exception as e:
        pass


    context = {
        "theme": theme,
        "today" : today,
        "socials": social,
        "ads_top": ads_top,
        "ads_left": ads_left,
        "admin_email": email,
        "admin_phone": phone,
        "web_site_name": name,
        "TreeNews": tree_news,
        "MainNews": main_news,
        "web_site_logo": logo,
        "reklama": _("Reklama"),
        "admin_address": address,
        "ads_bottom": ads_bottom,
        "ads_middle": ads_middle,
        "Categories": categories,
        "BreakingNews": breaking_news,
        "FeaturedNews": favorite_news,
        "web_site_favilcon": favilcon,
        "LastNewsTwo1": last_news_two_1,
        "LastNewsTwo2": last_news_two_2,
        "LastNewsTwo5": last_news_two_5,
        "LastNewsTwo6": last_news_two_6,
        "UzbekistanNews": uzbekistan_news,
        "comment_recapcha": FormWithCaptcha,
        "TheMostViewestdNews": the_most_viewest_news,
        "TheMostCommitedNews": the_most_commited_news,
        
        "com": _("Izoh"),
        "f_i_sh": ("F.I.SH"),
        "preview":_("Ortga"),
        "next":_("Keyingisi"),
        "news": _("Yangiliklar"),
        "send_btn": _("Yuborish"),
        "sections_name": _("Bo'limlar"),
        "subscribe": _("Obuna bo'ling"),
        "social_n": _("Bizni kuzating"),
        "w_comment": _("Izoh qoldirish"),
        "subscribe_1": _("Obuna bo'lish"),
        "all_news": _("Barcha Yangiliklar"),
        "full_n": _("To'liq ismingizni kiriting"),
        "t_v_news": _("Eng ko'p ko'rilgan yangiliklar"),
        "t_m_news": _("Eng ko'p muhokama qilingan yangiliklar"),
        "nothing":_("Afsuski bu sanada hech qanday malumot to'pilmadi"),
        "subscribe_2": _("Eng so'ngi yangiliklardan xabardor bo'ish uchun obuna bo'lishni unutmang."),
    }
    return context
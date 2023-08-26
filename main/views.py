from rest_framework import status
from django.utils import timezone
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    get_object_or_404,
    RetrieveUpdateDestroyAPIView,
)
from datetime import timedelta
from rest_framework.views import Response
from rest_framework.decorators import api_view
from .forms import ContactForm, FormWithCaptcha
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import render, get_object_or_404, redirect
from .models import (
    News, Ads,
    Comments, Category, MainNews, Subscribes
)
from .serializers import (
    CategoryMS, AdsMs,
    CommentMS, NewsMS, MainNewsSerializers
)
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.generic.list import ListView
from drf_spectacular.utils import extend_schema


# Create your views here.
""" GLOBAL VARIABLES """
now = timezone.now()
SevenDaysAgo = now - timedelta(days=7)


""" START CATEGORY VIEW """

class CategoryListView(ListAPIView):
    """ Hamma Category larni olish uchun """
    serializer_class = CategoryMS
    queryset = Category.objects.all().order_by("order_num")


class CategoryDetailView(RetrieveAPIView):
    """ Categorilarni DETAILNI olish uchun """
    serializer_class = CategoryMS
    queryset = Category.objects.all()


""" END CATEGORY VIEW """
""" START NEWS VIEW """

class PaginationNewsList(PageNumberPagination):
    """ PAGINATION CLASS FOR NEWS MODEL """
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 10000
    
    def get_paginated_response(self, data):
        return Response({
            "links":{
                "next": self.get_next_link(),
                "previous": self.get_previous_link()
            },
            "count":self.page.paginator.count,
            "total_pages": self.page.paginator.num_pages,
            "results": data
        })


class NewsListView(ListAPIView):
    """ HAMMA  YANGILIKLARNI OLISH UCHUN """
    serializer_class = NewsMS
    queryset = News.objects.filter(status="pub").order_by("-add_time")
    pagination_class = PaginationNewsList


class NewsListCategoriWithSlug(ListAPIView):
    """ YANGILIKLARNI CATEGORILARGA QARAB FILTERLAB OLISH UCHUN, 'CATEGORIANI "SLUG"I BILAN' """
    serializer_class = NewsMS
    queryset = News.objects.all()
    pagination_class = PaginationNewsList

    def get_queryset(self):
        slug = self.kwargs["slug"]
        if self.request is None:
            return News.objects.none()
        return News.objects.filter(status="pub", category__slug=slug).order_by("-add_time")


class BreakingNewsListView(ListAPIView):
    """ "BREAKING NEWS" BO'LIMI UCHUN 5TA TANLANGAN YANGILIK """
    serializer_class = NewsMS
    queryset = News.objects.filter(status="pub", breaking_news=True).order_by("-add_time")[:5]


class TheLastFiveNews(ListAPIView):
    """ BOSH SAHIFADAGI CARUSEL UCHUN 5TA ENG SO'NGI YANGILIKLAR """
    serializer_class = NewsMS
    queryset = News.objects.filter(status="pub").all().order_by("-add_time")[:5]


class UzbekistanInSevenDayFourNews(ListAPIView):
    """ BOSH SAHIFADAGI CARUSEL OLDIDAGI BO'LIM UCHUN 4TA UZBEKISTON YANGILIKLARI """
    serializer_class = NewsMS
    queryset = News.objects.filter(add_time__gte=SevenDaysAgo, add_time__lte=now, status="pub", uzbekiston_news=True).all().order_by("-add_time")[:4]


class TheMostReadNews(ListAPIView):
    """ ENG KO'P O'QILGAN 8ta YANGILIKLAR """
    serializer_class = NewsMS
    queryset = News.objects.filter(status="pub").order_by("-post_view")[:8]


class TheMostWriteCommenNews(ListAPIView):
    """ ENG KO'P KOMMENT YOZILGAN YANGILIKLAR """
    serializer_class = NewsMS 
    queryset = News.objects.all()

    def get_queryset(self):
        queryset = News.objects.filter(status="pub", comment_on_off=True).order_by("-comment_count")[:8]
        return queryset


class ChoicedCategoriesNews(ListAPIView):
    """ ASOSIY OYNADAGI TANLANGAN CATEGORIALAR UCHUN YANGILIKLAR """
    serializer_class = MainNewsSerializers
    queryset = MainNews.objects.all().order_by("order_num")


class TodayNews(ListAPIView):
    """ BUGUNGI YANGILIKLAR """
    serializer_class = NewsMS
    queryset = News.objects.filter(add_time=now, status="pub").order_by("-add_time")[:8]


class TheLastInSevenDaysNews(ListAPIView):
    """ OXIRGI 7 KUNLIK YANGILIKLAR """
    serializer_class = NewsMS
    queryset = News.objects.filter(add_time__gte=SevenDaysAgo, add_time__lte=now, status="pub").order_by("-add_time")[:8]


class TheLastIn30DaysNews(ListAPIView):
    """ OXIRGI 30KUNLIK YANGILIKLAR """
    serializer_class = NewsMS
    The30Day = now - timedelta(days=30)
    queryset = News.objects.filter(add_time__gte=The30Day, add_time__lte=now, status="pub").order_by("-add_time")[:8]


class NewsDetailView(RetrieveAPIView):
    """ YANGILIKNI DETAILNI OLISH UCHUN "ID" BILAN """
    serializer_class = NewsMS
    queryset = News.objects.filter(status="pub")


class NewsGETDetailWithSlug(RetrieveUpdateDestroyAPIView):
    """ YANGILIKNI DETAILNI OLISH UCHUN "SLUG" BILAN """
    serializer_class = NewsMS
    queryset = News.objects.all()

    def get_object(self, queryset=None, **kwargs):
        slug = self.kwargs.get("slug")
        return get_object_or_404(News.objects.filter(status="pub", slug=slug))


""" END NEWS VIEW """       

""" START COMMENT VIEW """


@extend_schema(request=None, responses=CommentMS)
@api_view(["POST", "GET"])
def Comment(request, news_id): 
    """ YANGILIKLARNING COMMENTARIASI UCHUN "ID" BILAN commentlarni olish uchun yangilik (news)ni ID sini jonatish kerak """
    if request.method == "GET":
        news = Comments.objects.filter(news=news_id).order_by("-add_time")
        serializer = CommentMS(news, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        comments = Comments.objects.filter(news=news_id).all()
        serializer = CommentMS(data=request.data)
        if serializer.is_valid():
            news_update = News.objects.get(id=news_id)
            news_update.comment_count = comments.count()
            news_update.comment_count + 1
            news_update.save()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


""" END COMMENT VIEW """

""" START ADS VIEW """

class AdsOnTopView(ListAPIView):
    """ WEB SAYTNI ENG YUQORISIDA TURADIGAN REKLAMAN """
    serializer_class = AdsMs
    queryset = Ads.objects.filter(status="pub", location="top") 


class AdsOnMiddleView(ListAPIView):
    """ WEB SAYTNI O'RTASIDA TURADIGAN REKLAMAN """
    serializer_class = AdsMs
    queryset = Ads.objects.filter(status="pub", location="middle") 


class AdsOnLeftView(ListAPIView):
    """ WEB SAYTNI YONLARIDA TURADIGAN REKLAMAN """
    serializer_class = AdsMs
    queryset = Ads.objects.filter(status="pub", location="left") 


class AdsOnBottomView(ListAPIView):
    """ WEB SAYTNI PASTIDA TURADIGAN REKLAMAN """
    serializer_class = AdsMs
    queryset = Ads.objects.filter(status="pub", location="bottom") 


""" END ADS VIEW """



""" TEMPLATES VIEWS """
from django.utils.translation import gettext_lazy as _

def Home(request):
    """ ASOSIY SAHIFA UCHUN FUNC """
    return render(request, "index.html")


def DetailNews(request, slug):
    """ YANGILIKLARNI DETAILNI OLISH UCHUN """
    news = get_object_or_404(News, slug=slug)
    news.post_view += 1
    news.save()  
    comments = Comments.objects.filter(news=news.id).all().order_by("-add_time")
    try:
        category_news = News.objects.filter(status="pub", category=news.category.id).order_by("-add_time")[10]
    except Exception as a:
        category_news = News.objects.filter(status="pub", category=news.category.id).order_by("-add_time")
    return render(request, "single.html", {"object" : news, "comments": comments, "category_news": category_news})


def FilterByCategory(request, id):
    """ YANGILIKLARNI CATEGORIASI BOYICHA FILTERLASH """
    ctg = Category.objects.get(id=id)
    news = News.objects.filter(status="pub", category=id).order_by("-add_time")
    paginator = Paginator(news, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "filter_by_category.htm", {"object_list": page_obj, "category": ctg})


def CreateComment(request):
    """ YANGILIKLAR UCHUN COMMENTARIA VA ULARNI HISOBLASH """
    if request.method == "POST":
        f_name = request.POST["f_name"]
        news_id = request.POST["news_id"] 
        comment = request.POST["comment"]
        path = request.POST["now_path"]
        news = News.objects.get(id=news_id)
        comments_count = Comments.objects.filter(news=news).count()
        comments = Comments.objects.create(
            news=news,
            f_name=f_name,
            comment=comment
        )
        comments.save()
        news.comment_count = 0
        news.comment_count += comments_count
        news.comment_count += 1
        news.save() 
        return redirect(f"{path}")
    return render(request, "comments.htm")


def SearchEngine(request):
    """ YANGILIKLARNI QIDIRISH """
    if request.method == "GET":
        try:
            query = request.GET["q"]
            news = News.objects.filter(Q(title__icontains=query), status="pub").order_by("-add_time")
        except Exception as e:
            news = News.objects.filter(status="pub").order_by("-add_time")
        context = {"object_list": news, "query": query}
    return render(request, "search_engine.htm", context)


class GetAllNewsList(ListView):
    """ HAMMA YANGILKLARNI OLISH """
    model = News
    paginate_by = 9
    ordering = "-add_time"
    template_name = "news.htm"


def FilterByDate(request, date):
    """ YANGILIKLARNI SANA BOYICHA FILTERLASH """
    news = News.objects.filter(status="pub", add_time__date=date).order_by("-add_time").all()
    return render(request, "filter_by_date.htm", {"object_list": news, "date": date})


def ContactUs(request):
    """ ADMIN BILAN BOG'LANISH """
    form = ContactForm
    if request.method == "POST":
        path = request.POST["now_path"]
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f'{path}')
        
    context = {
        "form": form,
        "a_a": _("Aloqa"),
        "recapcha": FormWithCaptcha,
        "m_s_y": _("Muallifga savol yollang"),
        "b_m":_("Bizni manzil"),
        "m_z":_("Toshkent shaxar Yunusobod 12 kv"),
        "e_p":_("E-Pochta"),
        "e_m":_("webmaster@yangisidan.uz"),
        "p_n":_("Telefon raqam"),
        "p_num":_("+998 33 000-00-00"),
        "j_t":_("Jonatish"),
    }
        
    return render(request, "contact.htm", context)
    

def subscribe(request):
    try:
        if request.method == "POST":
            email = request.POST.get("subscribe_email")
            sb = Subscribes.objects.create(
                email=email
            )
            sb.save()
            messages.success(request, _("Tabriklayman siz bizga obuna boldingiz :)"))
            return redirect("/")
    except Exception as e:
        messages.error(request, _("Afsuski sizni obuna qila olmadik biror muommo bolgan bo'lishi mumkun."))
        return redirect("/")
    
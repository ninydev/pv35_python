from django.http import JsonResponse
from django.shortcuts import render

from news.models import News


# Create your views here.
def news_list(request):

    page = request.GET.get('page', 1)
    per_page = request.GET.get('per_page', 6)
    # news_list = News.objects.all().order_by('-created_at')
    offset = (page - 1) * per_page

    news_list = News.objects.all().order_by('-created_at')[offset:offset + per_page]
    return render(request, 'news/news_list.html',
                  {'news_list': news_list,
                   'paginate': {'page': page, 'per_page': per_page}
                   })

def news_list_api(request):
    news_list = News.objects.all().order_by('-created_at')
    return JsonResponse({'news_list': list(news_list.values())})

def news_detail(request, news_id):
    news = News.objects.get(id=news_id)
    return render(request, 'news/news_detail.html', {'news': news})
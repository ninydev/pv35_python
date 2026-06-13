from django.http import JsonResponse
from django.shortcuts import render

from news.models import News


# Create your views here.
def news_list(request):
    news_list = News.objects.all().order_by('-created_at')
    return render(request, 'news/news_list.html', {'news_list': news_list})

def news_list_api(request):
    news_list = News.objects.all().order_by('-created_at')
    return JsonResponse({'news_list': list(news_list.values())})

def news_detail(request, news_id):
    news = News.objects.get(id=news_id)
    return render(request, 'news/news_detail.html', {'news': news})
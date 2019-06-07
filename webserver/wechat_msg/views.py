import random
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Content

def list_view(request):
    contents = Content.objects.all().order_by('-id')
    paginator = Paginator(contents, 50)
    page = request.GET.get('page')
    try:
        infos = paginator.page(page)
    except PageNotAnInteger:
        infos = paginator.page(1)
    except EmptyPage:
        infos = paginator.page(paginator.num_pages)
    prevPage = infos.number - 1
    hasPrev = infos.has_previous()
    nextPage = infos.number + 1
    hasNext = infos.has_next()
    return render(request, "wechat_msg/list.html", locals())

def content_view(request, content_id):
    content = Content.objects.get(id=content_id)
    # recommend = Content.objects.values("title","id").order_by("?")[:20]
    sample = random.sample(range(Content.objects.count()), 1)
    recommend = [Content.objects.values("title","id").get(id=i) for i in sample]
    return render(request, "wechat_msg/content.html", locals())

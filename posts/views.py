from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render
from .models import Post

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, 'pages/home.html', status=200)

def posts_list_view(request, *args, **kwargs):
    qs = Post.objects.all()
    posts_list = [{"id":x.id, "content":x.content} for x in qs]
    data = {
        "isUser":False,
        "response":posts_list,
    }
    return JsonResponse(data)

def post_detail_view(request, post_id, *args, **kwargs):
    data = {
        "id": post_id,
    }
    status = 200
    try:
        obj = Post.objects.get(id=post_id)
        data["content"] = obj.content
    except:
        data["message"] = "Not Found"
        status = 404
  
    return JsonResponse(data, status = status)

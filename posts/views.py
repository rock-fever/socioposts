from email import contentmanager
from django.http import  JsonResponse
from django.shortcuts import render, redirect
import random
from rest_framework.response import Response
from .models import Post
from .forms import PostForm
from django.conf import settings
from .serializers import PostSerializer, PostActionSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, 'pages/home.html', status=200)


@api_view(['POST'])
# @authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def post_create_view(request, *args, **kwargs):
    data = request.POST or None
    serializer = PostSerializer(data=request.POST)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)

@api_view(['GET'])
def post_detail_view(request, post_id, *args, **kwargs):
    qs = Post.objects.filter(id=post_id)
    if not qs.exists():
        return Response({}, status=404)
    obj = qs.first()
    serializer = PostSerializer(obj)
    return Response(serializer.data, status=200)

@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def post_delete_view(request, post_id, *args, **kwargs):
    qs = Post.objects.filter(id=post_id)
    if not qs.exists():
        return Response({}, status=404)
    qs = qs.filter(user=request.user)
    if not qs.exists():
        return Response({"message": "You cannot delete this post"}, status = 401)
    obj = qs.first()
    obj.delete()
    return Response({"message": "Post removed"}, status = 200)

@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def post_action_view(request, *args, **kwargs):
    serializer = PostActionSerializer(data = request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        post_id = data.get("id")
        action = data.get("action")

        qs = Post.objects.filter(id=post_id)
        if not qs.exists():
            return Response({}, status=404)
        obj = qs.first()
        if action == "like":
            obj.likes.add(request.user)
            serializer = PostSerializer(obj)
            return Response(serializer.data, status = 200)
        elif action == "unlike":
            obj.likes.remove(request .user)
        elif action == "retweet":
            pass 
    return Response({}, status = 200)


@api_view(['GET'])
def posts_list_view(request, *args, **kwargs):
    qs = Post.objects.all()
    serializer = PostSerializer(qs, many=True)
    return Response(serializer.data)

def post_create_view_pure_django(request, *args, **kwargs):

    user = request.user 
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = PostForm(request.POST or None)
    next_url = request.POST.get('next')
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = request.user
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)
        if next_url != None:
            return redirect(next_url)
        form = PostForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context = {'form': form}) 


def posts_list_view_pure_django(request, *args, **kwargs):
    qs = Post.objects.all()
    posts_list = [x.serialize() for x in qs]
    data = {
        "isUser":False,
        "response":posts_list,
    }
    return JsonResponse(data)

def post_detail_view_pure_django(request, post_id, *args, **kwargs):
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

from django.urls import path
from .views import (
    post_detail_view, 
    posts_list_view,
    post_create_view,
    post_action_view,
    post_delete_view
    )
urlpatterns = [
    path('', posts_list_view),
    path('action/', post_action_view),
    path('create/', post_create_view),
    path('<int:post_id>/', post_detail_view),
    path('<int:post_id>/delete/', post_delete_view)
]

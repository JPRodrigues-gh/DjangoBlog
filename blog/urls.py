""" urls.py file in blog folder """
from . import views
from django.urls import path


# using class-based views we need to add the as_view method on the
#  end of post list. So it's going to render this class as a view.
urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
]

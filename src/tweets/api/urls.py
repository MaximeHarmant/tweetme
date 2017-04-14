from django.conf.urls import url

from .views import TweetListAPIView, TweetCreateAPIView, RetweetAPIView, LikeToggleAPIView, TweetDetailAPIView

urlpatterns = [
    url(r'^$', TweetListAPIView.as_view(), name='list'),  # /api/tweet/
    url(r'^create/$', TweetCreateAPIView.as_view(), name='create'),  # /api/tweet/create/
    url(r'^(?P<pk>\d+)/$', TweetDetailAPIView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/like/$', LikeToggleAPIView.as_view(), name='like'),
    url(r'^(?P<pk>\d+)/retweet/$', RetweetAPIView.as_view(), name='retweet'),
]

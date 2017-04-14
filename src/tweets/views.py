from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .form import TweetModelForm
from .mixins import FormUserNeededMixin, UserOwnerMixin
from .models import Tweet


# Create your views here.
class RetweetView(View):
    def get(self, request, pk, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=pk)
        if request.user.is_authenticated():
            new_tweet = Tweet.objects.retweet(request.user, tweet)
            return HttpResponseRedirect('/')
        return HttpResponseRedirect(tweet.get_absolute_url())


class TweetCreateView(FormUserNeededMixin, CreateView):
    form_class = TweetModelForm
    template_name = 'tweets/create_view.html'


class TweetUpdateView(LoginRequiredMixin, UserOwnerMixin, UpdateView):
    queryset = Tweet.objects.all()
    form_class = TweetModelForm
    template_name = 'tweets/update_view.html'


class TweetDeleteView(LoginRequiredMixin, DeleteView):
    queryset = Tweet.objects.all()
    success_url = reverse_lazy('tweet:list')


class TweetDetailView(DetailView):
    queryset = Tweet.objects.all()


class TweetListView(LoginRequiredMixin, ListView):
    queryset = Tweet.objects.all()

    def get_queryset(self):
        qs = Tweet.objects.all()
        query = self.request.GET.get('q', None)
        if query is not None:
            qs = qs.filter(
                Q(content__icontains=query) |
                Q(user__username__icontains=query)
            )
        return qs

    def get_context_data(self, **kwargs):
        context = super(TweetListView, self).get_context_data(**kwargs)
        context['create_form'] = TweetModelForm()
        context['create_url'] = reverse_lazy('tweet:create')
        return context


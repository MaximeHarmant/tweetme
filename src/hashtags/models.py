from django.db import models

# Create your models here.
from django.urls import reverse_lazy
from tweets.models import Tweet

from hashtags.signals import parsed_hastags


class HashTag(models.Model):
    tag = models.CharField(max_length=120)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse_lazy('hashtag', kwargs={'hastag': self.tag})

    def get_tweets(self):
        return Tweet.objects.filter(content__icontains='#'+self.tag)


def parsed_hastags_receiver(sender, hashtag_list, *args, **kwargs):
    if len(hashtag_list):
        for tag in hashtag_list:
            new_tag, created = HashTag.objects.get_or_create(tag=tag)

parsed_hastags.connect(parsed_hastags_receiver)
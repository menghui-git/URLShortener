from datetime import datetime, timedelta

from django.db import models, IntegrityError
from django.utils import timezone

from shortener.caches import URLCache
from shortener.utils import generate_random_code


class URLManagement(models.Manager):
    def save_url(self, url):
        hash = URLCache.get_hash(url)
        if hash:
            return hash

        while True:
            try:
                hash = generate_random_code()
                self.create(hash=hash, url=url)
                hash_url_pairs = ((hash, url),)
                URLCache.set(hash_url_pairs)
                break   # main conditions #1
            except IntegrityError as e:
                if 'Key (url)' in str(e):
                    return self.get(url=url).hash
        return hash

    def get_url(self, hash):
        url = URLCache.get_url(hash)  # main conditions #2
        if not url:
            try:
                url = self.get(hash=hash).url
            except URL.DoesNotExist:
                return None
            hash_url_pairs = ((hash, url),)
            URLCache.set(hash_url_pairs)
        return url

    def delete_expired_urls(self, days=1):
        now = datetime.now()
        expired_at = timezone.make_aware(
            datetime(now.year, now.month, now.day) - timedelta(days=days),
            timezone=timezone.get_current_timezone()
        )
        self.filter(created_at__lte=expired_at).delete()
        hash_url_pairs = self.order_by('-created_at')[:100].values_list('hash', 'url')
        URLCache.set(hash_url_pairs)


class URL(models.Model):
    URL_MAX_LENGTH = 200

    objects = URLManagement()

    hash = models.CharField(max_length=8, blank=False, null=False, unique=True)
    url = models.URLField(max_length=URL_MAX_LENGTH, blank=False, null=False, unique=True)
    created_at = models.DateTimeField(auto_now=True)

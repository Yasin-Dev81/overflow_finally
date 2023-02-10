import time

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


def blog_cover_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'covers/{0}.png'.format(time.ctime())


class Blog(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()

    cover = models.ImageField(upload_to=blog_cover_directory_path, blank=False)

    download_url = models.URLField(verbose_name="download url")

    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    is_active = models.BooleanField(default=False)

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('detail_view_url', args=[self.pk, ])

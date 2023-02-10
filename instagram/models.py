from django.db import models
from django.urls import reverse
from jsonfield import JSONField


class MyInstaPage(models.Model):
    user_key = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    user_id = models.CharField(max_length=20)
    settings = JSONField()

    def __str__(self):
        return '%s' % self.username


class InstaUserForCopy(models.Model):
    username = models.CharField(max_length=30, verbose_name="username for coping")
    user_id = models.CharField(max_length=30, verbose_name="user id for coping")

    user_pub = models.ForeignKey(MyInstaPage, on_delete=models.CASCADE, verbose_name="my user for public")

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('home_url')


class InstaPkForCopy(models.Model):
    insta_pk = models.IntegerField()
    status_tupel = (
        ('pub', 'published'),
        ('drf', 'draft'),
    )
    status = models.CharField(choices=status_tupel, max_length=10)

    user_pub = models.ForeignKey(MyInstaPage, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.insta_pk)

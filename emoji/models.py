from django.contrib.auth.models import AbstractUser
from django.db import models


# User = get_user_model()


class User(AbstractUser):
    # 使用外键扩展user表
    wechat = models.CharField(max_length=30)


# Create your models here.
class Emoji(models.Model):
    type = models.CharField(max_length=200)
    path = models.TextField()


class EmojiSeries(models.Model):
    name = models.CharField(max_length=200)
    url = models.TextField()
    path = models.TextField()
    num = models.IntegerField()

    def __str__(self):
        return self.name


class SeriesElement(models.Model):
    series = models.ForeignKey(EmojiSeries, on_delete=models.CASCADE)
    url = models.TextField()
    path = models.TextField()

    def __str__(self):
        return self.path.split('/')[-1][:-4]


class Tag(models.Model):
    name = models.CharField(max_length=200)
    hits = models.IntegerField(default=0)

    class Meta:
        # hits降序，name升序
        ordering = ['-hits']

    def __str__(self):
        return self.name


class AsciiEmoji(models.Model):
    content = models.CharField(max_length=100)
    tag = models.ForeignKey(Tag, related_name='emojis', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.content


class Material(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=400)
    path = models.CharField(max_length=300)
    filetype = models.CharField(max_length=50)

    def __str__(self):
        return self.name

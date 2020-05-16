from django.db import models
from django.conf import settings

USER = settings.AUTH_USER_MODEL


class Contest(models.Model):
    contest_title = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False)
    creator = models.ForeignKey(USER, on_delete=models.CASCADE, related_name="creator")
    contest_description = models.TextField(max_length=300, default="")
    contest_image = models.ImageField(null=True, blank=True)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.contest_title


class Choice(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    choice_picture = models.ImageField(null=True, blank=True)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

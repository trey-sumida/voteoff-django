from django.db import models
from django.conf import settings

USER = settings.AUTH_USER_MODEL

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False)
    creator = models.ForeignKey(USER, on_delete=models.CASCADE, related_name='creator')

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

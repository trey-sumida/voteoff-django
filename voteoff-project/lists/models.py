from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField("UserProfile", blank=True)

def post_save_user_model_receiver(sender, instance, created, *args, **kwargs):
    if created:
        try:
            UserProfile.objects.create(user=instance)
        except:
            pass

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class Friend(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user', default=None)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user', default=None)
    accepted = models.BooleanField(default=False)


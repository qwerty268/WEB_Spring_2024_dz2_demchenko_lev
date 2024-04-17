from django.contrib.auth.models import User
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    rating = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class QuestionLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'question')


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    Profile = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    rating = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AnswerLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'answer')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    avatar = models.ImageField(null=True, blank=True)
    nick_name = models.CharField(max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

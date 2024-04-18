from collections import Counter
from typing import Tuple, Any

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count, QuerySet


class QuestionManager(models.Manager):

    def get_new(self):
        return self.order_by('-created_at')

    def get_hot(self):
        return self.order_by('-rating', 'created_at')

    def get_by_tag(self, tag):
        tag_id = Tag.objects.get(name=tag).id
        return self.filter(tags=tag_id)

    def get_by_id(self, question_id):
        return self.get(pk=question_id)


class TagManager(models.Manager):

    def get_popular_tags(self):
        queryset = Question.objects.values('tags')

        # Преобразуем QuerySet в список значений
        values = [item['tags'] for item in queryset]

        count_dict = Counter(values)

        # Сортируем словарь по убыванию значений
        sorted_counts = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)[:5]

        pks = []

        for value in sorted_counts[:5]:
            pks.append(value[0])

        return self.filter(id__in=pks)


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    objects = TagManager()

    def __str__(self):
        return self.name


class Question(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = QuestionManager()

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text


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

    def __str__(self):
        return self.nick_name

import random
import time

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from app.models import Profile, Question, Tag, Answer, QuestionLike, AnswerLike


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **options):
        ratio = options['ratio']

        users = []
        profiles = []
        for i in range(ratio):
            user = User(username=f'Имя пользователя {i}')
            users.append(user)
            profiles.append(Profile(user=user, nick_name=f'Никнейм {i}'))

        User.objects.bulk_create(users)
        Profile.objects.bulk_create(profiles)

        tags = []
        for i in range(ratio):
            tag = Tag(name=f'tag {i}')
            tags.append(tag)
            tag.save()

        questions = []
        for i in range(ratio * 10):
            question = Question(id=i, user=users[i // 10], title=f'Вопрос {i}', text=f'текст вопроса {i}')
            question.save()
            question.tags.add(tags[(i - 1) // 10])
            questions.append(question)

        likes = []
        for i in range(ratio):
            for j in range(ratio * 10):
                likes.append(QuestionLike(user=users[i], question=questions[j]))
        QuestionLike.objects.bulk_create(likes)

        #всего вопросов ratio * 10
        answers = []
        for i in range(ratio):
            for j in range(ratio * 10):
                answers.append(Answer(question=questions[j], user=users[i], text=f'ответ {i * j}', is_correct=bool(i % 3)))
        Answer.objects.bulk_create(answers)

        #всего ответов ratio * ratio * 10
        likes = []
        for i in range(ratio):
            for j in range(ratio * ratio * 10):
                likes.append(AnswerLike(user=users[i], answer=answers[j]))
        AnswerLike.objects.bulk_create(likes)

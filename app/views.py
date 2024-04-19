from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render

from app.models import QuestionManager, Question, Answer


# Create your views here.
def get_pagination(request, items):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(items, 3, error_messages={"no_results": "Page does not exist"}, )
    try:
        page_obj = paginator.page(page_num)
    except (EmptyPage, PageNotAnInteger):
        return paginator.page(1)
    return page_obj


def hot(request):
    page_obj = get_pagination(request, Question.objects.get_hot())
    return render(request, 'hot.html', {"questions": page_obj})


def newest(request):
    page_obj = get_pagination(request, Question.objects.get_new())
    return render(request, 'new_questions.html', {"questions": page_obj})


def user_settings(request):
    return render(request, 'user_settings.html')


def question(request, question_id):
    item = Question.objects.get_by_id(question_id)
    answers = Answer.objects.filter(question=question_id)
    return render(request, 'question_detail.html', {"question": item, "answers": answers})


def login(request):
    return render(request, 'login.html')


def registration(request):
    return render(request, 'registration.html')


def ask(request):
    return render(request, 'add_question_page.html')


def get_by_tag(request, tag):
    questions = Question.objects.get_by_tag(tag)
    return render(request, 'search_qeustions_by_tag.html', {"questions": questions, "tag": tag})


def logout(request):
    return render(request, 'login.html')

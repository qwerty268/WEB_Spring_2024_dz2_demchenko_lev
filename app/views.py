from django.contrib import auth
from django.contrib.auth import authenticate, logout, login
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, Http404, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from app.forms import LoginForm, RegistrationForm
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


@require_http_methods(['GET', 'POST'])
def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)

        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            if user is not None:
                login(request, user)
                return redirect(reverse('newest'))
            else:
                login_form.add_error(None, "Ошибка в логине или в пароле")
                return render(request, 'login.html',
                              {"form": login_form})
        else:
            login_form.add_error(login_form.username, "Некорректно введены данные")
            return render(request, 'login.html',
                          {"form": login_form})

    login_form = LoginForm()
    return render(request, 'login.html', {"form": login_form})


@require_http_methods(['GET', 'POST'])
def registration(request):
    if request.method == 'GET':
        return render(request, 'registration.html', {"form": RegistrationForm()})
    else:
        user_form = RegistrationForm(request.POST, request.FILES)
        if user_form.is_valid():
            user = user_form.save()
            if user:
                login(request, user)
                return redirect(reverse('newest'))
            else:
                user_form.add_error(None, "User saving error")
    return render(request, 'registration.html', {'form': user_form})


def ask(request):
    return render(request, 'add_question_page.html')


def get_by_tag(request, tag):
    questions = Question.objects.get_by_tag(tag)
    return render(request, 'search_qeustions_by_tag.html', {"questions": questions, "tag": tag})


def logout_view(request):
    logout(request)

    return redirect(reverse('login'))



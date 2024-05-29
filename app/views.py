from django.contrib.auth import authenticate, logout, login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from app.forms import LoginForm, RegistrationForm, EditProfileForm, QuestionForm, AnswerForm
from app.models import Question, Answer


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


@require_http_methods(['GET', 'POST'])
def user_settings(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user = request.user
            return render(request, 'user_settings.html',
                          {'form': EditProfileForm(initial={'username': user.username, 'email': user.email})})
        else:
            return redirect(reverse('login'))
    else:
        print(request.FILES)
        edit_form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            user = edit_form.save()
            if user:
                return render(request, 'user_settings.html',
                              {'form': EditProfileForm(initial={'username': user.username, 'email': user.email})})
            else:
                edit_form.add_error(None, "User updating error")
        return render(request, 'user_settings.html', {'form': edit_form})


def question(request, question_id):
    item = Question.objects.get_by_id(question_id)
    if request.method == 'GET':
        answers = Answer.objects.filter(question=question_id)
        return render(request, 'question_detail.html',
                      {"question": item, "answers": answers, 'form': AnswerForm()})
    else:
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            user = request.user
            answer_form.save_with_related_data(user, item)
            answers = Answer.objects.filter(question=question_id)
            return render(request, 'question_detail.html',
                          {"question": item, "answers": answers, 'form': AnswerForm()})
        else:
            answers = Answer.objects.filter(question=question_id)
            return render(request, 'question_detail.html',
                          {"question": item, "answers": answers, 'form': answer_form})



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


@require_http_methods(['GET', 'POST'])
def ask(request):
    if request.method == 'GET':
        return render(request, 'add_question_page.html', {'form': QuestionForm()})
    else:
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question_form.save_with_related_data(request.user)
            return redirect(reverse('newest'))
        else:
            return render(request, 'add_question_page.html', {'form': question_form})


def get_by_tag(request, tag):
    questions = Question.objects.get_by_tag(tag)
    return render(request, 'search_qeustions_by_tag.html', {"questions": questions, "tag": tag})


def logout_view(request):
    logout(request)
    return redirect(reverse('login'))

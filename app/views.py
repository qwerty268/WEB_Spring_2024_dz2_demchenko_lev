from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

QUESTIONS = [
    {
        "id": i,
        "title": f"lol {i}",
        "text": f"This is question number {i}",
        "tags": ["tag1", "tag2", "tag3"]

    } for i in range(100)
]


def hot(request):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(QUESTIONS, 3)
    page_obj = paginator.page(page_num)
    return render(request, 'hot.html', {"questions": page_obj})


def newest(request):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(QUESTIONS, 3)
    page_obj = paginator.page(page_num)
    return render(request, 'new_questions.html', {"questions": page_obj})


def user_settings(request):
    return render(request, 'user_settings.html')


def question(request, question_id):
    item = QUESTIONS[question_id]
    answers = [
        {
            "text": "answer1"
        },
        {
            "text": "answer2"
        }
    ]
    return render(request, 'question_detail.html', {"question": item, "answers": answers})


def login(request):
    return render(request, 'login.html')


def registration(request):
    return render(request, 'registration.html')


def ask(request):
    return render(request, 'add_question_page.html')


def get_by_tag(request, tag):
    questions = []
    for question in QUESTIONS:
        if tag in question.get("tags"):
            questions.append(question)
    return render(request, 'search_qeustions_by_tag.html', {"questions": questions, "tag": tag})
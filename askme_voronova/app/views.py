from django.core.paginator import Paginator
from django.shortcuts import render

from app.models import *

# Create your views here.

best_users = Profile.objects.best_users()
best_tags = Tag.objects.best_tags()

context = {
        'best_users': best_users,
        'best_tags': best_tags,
}


def pagination(page_type, request, limit):
    paginator = Paginator(page_type, limit)
    page = request.GET.get('page')
    content = paginator.get_page(page)
    return content


def index(request):
    questions = Question.objects.new_questions()
    content = pagination(questions, request, 5)
    context['questions'] = questions,
    return render(request, "index.html", {'content': content, 'context': context})


def hot(request):
    questions = Question.objects.hot_questions()
    content = pagination(questions, request, 5)
    context['questions'] = questions,
    return render(request, "hot.html", {'content': content, 'context': context})


def question(request, number):
    question = Question.objects.get(id=number)
    answers = Answer.objects.get_answers(number)
    content = pagination(answers, request, 5)
    context['number'] = number
    context['question'] = question
    return render(request, "question.html", {'content': content, 'context': context})


def login(request):
    return render(request, "login.html", {'context': context})


def ask(request):
    return render(request, "ask.html", {'context': context})


def settings(request):
    return render(request, "settings.html", {'context': context})


def signup(request):
    return render(request, "signup.html", {'context': context})


def tag(request, name):
    questions = Question.objects.tag_questions(name)
    content = pagination(questions, request, 5)
    context['name'] = name
    context['question'] = question
    return render(request, "tag.html", {'content': content, 'context': context})


def error(request):
    return render(request, "404.html", {})

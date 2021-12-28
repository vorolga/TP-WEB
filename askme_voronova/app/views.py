from django.contrib import auth
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

from app.models import *
from app.forms import *

# Create your views here.

context = {}

def definition(context):
    best_users = Profile.objects.best_users()
    best_tags = Tag.objects.best_tags()
    context['best_tags'] = best_tags
    context['best_users'] = best_users


def pagination(page_type, request, limit):
    paginator = Paginator(page_type, limit)
    page = request.GET.get('page')
    content = paginator.get_page(page)
    return content


def index(request):
    definition(context)
    questions = Question.objects.new_questions()
    content = pagination(questions, request, 5)
    context['questions'] = questions,
    return render(request, "index.html", {'content': content, 'context': context})


def hot(request):
    definition(context)
    questions = Question.objects.hot_questions()
    content = pagination(questions, request, 5)
    context['questions'] = questions,
    return render(request, "hot.html", {'content': content, 'context': context})


def question(request, number):
    definition(context)
    question = Question.objects.get(id=number)
    answers = Answer.objects.get_answers(number)
    content = pagination(answers, request, 5)
    context['number'] = number
    context['question'] = question
    return render(request, "question.html", {'content': content, 'context': context})


def login(request):
    global form
    definition(context)
    print(request.POST)
    if request.method == 'GET':
        form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = auth.authenticate(**form.cleaned_data)
            if not user:
                form.add_error(None, "User not found")
            else:
                auth.login(request, user)
                return redirect(reverse('index'))
    return render(request, "login.html", {'context': context, 'form': form})


def ask(request):
    definition(context)
    return render(request, "ask.html", {'context': context})


def settings(request):
    definition(context)
    return render(request, "settings.html", {'context': context})


def signup(request):
    definition(context)
    return render(request, "signup.html", {'context': context})


def tag(request, name):
    definition(context)
    questions = Question.objects.tag_questions(name)
    content = pagination(questions, request, 5)
    context['name'] = name
    context['question'] = question
    return render(request, "tag.html", {'content': content, 'context': context})


def error(request):
    definition(context)
    return render(request, "404.html", {})

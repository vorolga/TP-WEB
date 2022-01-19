import jwt
from cent import Client
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from app.models import *
from app.forms import *
from askme.settings import CENTRIFUGO_SECRET_KEY, CENTRIFUGO_API_KEY

# Create your views here.

context = {}

cl = Client("http://127.0.0.1:8000/api", api_key=CENTRIFUGO_API_KEY, timeout=1)


def context_processor(request):
    context["best_users"] = cache.get('best_users')
    context["best_tags"] = cache.get('best_tags')
    return context


# def definition(context):
#     best_users = Profile.objects.best_users()
#     best_tags = Tag.objects.best_tags()
#     context['best_tags'] = best_tags
#     context['best_users'] = best_users


def pagination(page_type, request, limit):
    paginator = Paginator(page_type, limit)
    page = request.GET.get('page')
    content = paginator.get_page(page)
    return content


def index(request):
    # definition(context)
    questions = Question.objects.new_questions()
    content = pagination(questions, request, 5)
    context['questions'] = questions
    profile = None

    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None

    if profile is not None:
        context['question_liked'] = list(
            QuestionRating.objects.values_list('question_id', flat=True).filter(user=request.user.profile, mark=1))
        context['question_disliked'] = list(
            QuestionRating.objects.values_list('question_id', flat=True).filter(user=request.user.profile, mark=-1))

    return render(request, "index.html", {'content': content, 'context': context})


def hot(request):
    # definition(context)
    questions = Question.objects.hot_questions()
    content = pagination(questions, request, 5)
    context['questions'] = questions
    profile = None

    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None

    if profile is not None:
        context['question_liked'] = list(
            QuestionRating.objects.values_list('question_id', flat=True).filter(user=request.user.profile, mark=1))
        context['question_disliked'] = list(
            QuestionRating.objects.values_list('question_id', flat=True).filter(user=request.user.profile, mark=-1))

    return render(request, "hot.html", {'content': content, 'context': context})


def question(request, number):
    # definition(context)
    global form
    question = Question.objects.get(id=number)
    context['number'] = number
    context['question'] = question
    context['new_answer'] = ""

    profile = None

    if request.user.is_authenticated:
        context['cent_token'] = jwt.encode({"sub": str(request.user.id)}, CENTRIFUGO_SECRET_KEY)
        context['cent_chan'] = f"question_{question.id}"
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None

    if request.method == "GET":
        form = AnswerForm()

    if request.method == "POST":
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            answer = Answer.objects.create(question_id=number,
                                           author=profile,
                                           text=form.cleaned_data["text"])
            answers = Answer.objects.get_answers(number)
            context['new_answer'] = answer
            content = pagination(answers, request, 5)
            cl.publish(f"question_{question.id}", {"answer": model_to_dict(answer)})
            return redirect(reverse("question", kwargs={"number": number}) + "?page="
                            + str(content.paginator.num_pages) + f"#{answer.id}")

    answers = Answer.objects.get_answers(number)

    if profile is not None:
        context['question_liked'] = QuestionRating.objects.filter(question=question, user=request.user.profile,
                                                                  mark=1).count()
        context['question_disliked'] = QuestionRating.objects.filter(question=question, user=request.user.profile,
                                                                     mark=-1).count()

        context['user'] = request.user.profile
        context['answer_liked'] = []
        context['answer_disliked'] = []
        for answer in answers:
            if AnswerRating.objects.filter(answer=answer, user=request.user.profile, mark=1).count():
                context['answer_liked'].append(answer.id)
            if AnswerRating.objects.filter(answer=answer, user=request.user.profile, mark=-1).count():
                context['answer_disliked'].append(answer.id)

    content = pagination(answers, request, 5)
    return render(request, "question.html", {'content': content, 'context': context, 'form': form})


def login(request):
    global form
    # definition(context)
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


@login_required
def ask(request):
    global form
    # definition(context)
    if request.method == "GET":
        form = AskForm()
    if request.method == "POST":
        form = AskForm(data=request.POST)
        if form.is_valid():
            tags = form.save()
            user = request.user.id
            profile = Profile.objects.get(user_id=user)
            question = Question.objects.create(author=profile,
                                               title=form.cleaned_data["title"],
                                               text=form.cleaned_data["text"])
            for tag in tags:
                question.tags.add(tag)
                question.save()
            return redirect("question", question.id)
    return render(request, "ask.html", {'context': context, 'form': form})


@login_required
def settings(request):
    global form
    # definition(context)
    if request.method == 'GET':
        form = SettingsForm(data={"username": request.user.username, "email": request.user.email})
    if request.method == 'POST':
        form = SettingsForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = request.user
            if form.cleaned_data["old_password"] != "":
                if not user.check_password(form.cleaned_data["old_password"]):
                    form.add_error(None, "Old password is wrong!")
                if form.cleaned_data["password"] != form.cleaned_data["password_repeat"] or form.cleaned_data[
                    "password"] == "":
                    form.add_error(None, "New passwords do not match!")
                user.set_password(form.cleaned_data["password"])
                user.save()
                auth.login(request, user)
            else:
                if form.cleaned_data["password"] != "" or form.cleaned_data["password_repeat"] != "":
                    form.add_error(None, "You must write old password!")

            if form.cleaned_data["username"] != user.username and form.cleaned_data["username"] != "":
                p = list(User.objects.values_list("username", flat=True))
                username = form.cleaned_data["username"]
                if username in p:
                    form.add_error(None, "This username is already used!")
                user.username = form.cleaned_data["username"]
                user.save()
                auth.login(request, user)
                Profile.objects.filter(user=user).update(login=user.username)
            if form.cleaned_data["email"] != user.email and form.cleaned_data["email"] != "":
                user.email = form.cleaned_data["email"]
                user.save()
                auth.login(request, user)
            if form.files.get("avatar"):
                user.profile.avatar = form.files.get("avatar")
                user.profile.save()
    return render(request, "settings.html", {'context': context, 'form': form})


def signup(request):
    global form
    # definition(context)
    if request.method == "GET":
        form = SignUpForm()

    if request.method == "POST":
        form = SignUpForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save()
            if user is not None:
                if form.files.get("avatar"):
                    user.profile.avatar = form.files.get("avatar")
                    user.profile.save()
                auth.login(request, user)
                return redirect("index")
    return render(request, "signup.html", {'context': context, 'form': form})


def tag(request, name):
    # definition(context)
    questions = Question.objects.tag_questions(name)
    content = pagination(questions, request, 5)
    context['name'] = name
    context['question'] = question
    return render(request, "tag.html", {'content': content, 'context': context})


def error(request):
    # definition(context)
    return render(request, "404.html", {})


@login_required
def logout(request):
    auth.logout(request)
    return redirect("index")


@login_required
@require_POST
def vote(request):
    id = request.POST['id']
    action = request.POST['action']
    model = request.POST['model']

    if model == "question":
        Question.objects.change_rating(id, action, request.user.profile)
        return JsonResponse({'rating': Question.objects.get(id=id).rating})

    if model == "answer":
        Answer.objects.change_rating(id, action, request.user.profile)
        return JsonResponse({'rating': Answer.objects.get(id=id).rating})


@login_required
@require_POST
def correct(request):
    answer_id = request.POST['id']
    Answer.objects.change_correct(answer_id, request.user.profile.id)
    return JsonResponse({'correct': Answer.objects.get(id=answer_id).is_correct})

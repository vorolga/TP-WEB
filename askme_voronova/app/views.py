from django.core.paginator import Paginator
from django.shortcuts import render


# Create your views here.


questions = [
    {
        "title": f"What is Bootstrap?",
        "text": f"Bootstrap — свободный набор инструментов для создания сайтов и веб-приложений. Включает в себя HTML- и CSS-шаблоны оформления для типографики, веб-форм, кнопок, меток, блоков навигации и прочих компонентов веб-интерфейса, включая JavaScript-расширения.",
        "number": i
    } for i in range(100)
]

answers = [
    {
        "text": f"Bootstrap — свободный набор инструментов для создания сайтов и веб-приложений. Включает в себя HTML-и CSS-шаблоны оформления для типографики, веб-форм, кнопок, меток, блоков навигации и прочих компонентов веб-интерфейса, включая JavaScript-расширения. Bootstrap — свободный набор инструментов для создания сайтов и веб-приложений. Включает в себя HTML- и CSS-шаблоны оформления для типографики, веб-форм, кнопок, меток, блоков навигации и прочих компонентов веб-интерфейса, включая JavaScript-расширения.  Bootstrap — свободный набор инструментов для создания сайтов и веб-приложений. Включает в себя HTML- и CSS-шаблоны оформления для типографики, веб-форм, кнопок, меток, блоков навигации и прочих компонентов веб-интерфейса, включая JavaScript-расширения.",
        "number": i
    } for i in range(10)
]


def pagination(page_type, request, limit):
    paginator = Paginator(page_type, limit)
    page = request.GET.get('page')
    content = paginator.get_page(page)
    return content


def index(request):
    return render(request, "index.html", {'questions': pagination(questions, request, 5)})


def hot(request):
    return render(request, "hot.html", {'questions': pagination(questions, request, 5)})


def question(request, number):
    return render(request, "question.html", {'number': questions[number], 'answers': pagination(answers, request, 3)})


def login(request):
    return render(request, "login.html", {})


def ask(request):
    return render(request, "ask.html", {})


def settings(request):
    return render(request, "settings.html", {})


def signup(request):
    return render(request, "signup.html", {})


def tag(request, name):
    return render(request, "tag.html", {'questions': pagination(questions, request, 5)})

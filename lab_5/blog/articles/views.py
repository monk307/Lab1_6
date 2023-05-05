from .models import Article
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.models import User

def auth(request):
    if request.user.is_anonymous:
        if request.method == "POST":
            form = {'username': request.POST["username"], 'password': request.POST["password"]}

            if '' in form.values():
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'auth.html', {'form': form})

            user = authenticate(username=request.POST["username"], password=request.POST["password"])

            if user:
                login(request, user)
                return redirect('/')
            else:
                form['errors'] = u"Извините, пользователь не найден..."
                return render(request, 'auth.html', {'form': form})
        else:
            return render(request, 'auth.html', {})
    else:
        return render(request, 'forbidden.html', {})


def registration(request):
    if request.user.is_anonymous:
        if request.method == "POST":

            form = {
                'username': request.POST["username"],
                'email': request.POST["email"],
                'password': request.POST["password"],
                'password_confirm': request.POST["password_confirm"],
            }

            if '' in form.values():
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'registration.html', {'form': form})
            elif form['password'] != form['password_confirm']:
                form['errors'] = u"Пароли не совпадают"
                return render(request, 'registration.html', {'form': form})

            User.objects.create_user(form['username'], form['email'], form['password'])
            return redirect('/')
        else:
            return render(request, 'registration.html', {})
    else:
        return render(request, 'forbidden.html', {})

def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})


def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404

def create_post(request):
    if not request.user.is_anonymous:
        if request.method == "POST":
            form = {'text': request.POST["text"], 'title': request.POST["title"]}

            # Проверка на уникальность титульника
            if Article.objects.filter(title=form["title"]).first():
                form['errors'] = u"Название новости не уникально..."
                return render(request, 'create_post.html', {'form': form})

            if form["text"] and form["title"]:
                result = Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                return redirect('get_article', article_id=result.id)
            else:
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'create_post.html', {'form': form})
        else:
            return render(request, 'create_post.html', {})
    else:
        raise Http404

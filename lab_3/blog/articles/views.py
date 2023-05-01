from django.shortcuts import render

# Create your views here.
from .models import Article
def archive(request):
    return render(request, 'archive.html', {"posts": Article.objects.all()})

from django.shortcuts import render
from .models import AddTP
from django.http import HttpResponse


def index(request):
    return render(request, 'tplibrary/index.html', {})
def addtp(request):
    if request.method == 'POST':
        author = request.POST['author']
        book_title = request.POST['title']
        description = request.POST['desc']
        if len(author) < 3:
            return HttpResponse('Error, author name is too short')
        else:
            new_book = AddTP(author = author, title = book_title, description = description)
            new_book.save()
    return render(request, 'tplibrary/addtp.html', {})

def data(request):
    Addtps = AddTP.objects.all()
    return render(request, 'tplibrary/data.html', {'Addtps' : Addtps})

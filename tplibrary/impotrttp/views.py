from django.shortcuts import render, redirect
from .models import AddTP
from .forms import AddTPForm
from django.http import HttpResponse

def index(request):
    return render(request, 'tplibrary/index.html', {})

def addtp(request):
    if request.method == 'POST':
        form = AddTPForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('data')
        else:
            return HttpResponse('Error, form is not valid')
    else:
        form = AddTPForm()
    return render(request, 'tplibrary/addtp.html', {'form': form})

def data(request):
    addtps = AddTP.objects.all()
    return render(request, 'tplibrary/data.html', {'addtps': addtps})
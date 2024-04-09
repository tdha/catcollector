from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Cat

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def cats_index(request):
    cats = Cat.objects.all()
    return render(request, 'cats/index.html', {
        'cats': cats
    })

def cats_detail(request, cat_id):
    cat = Cat.objects.get(id=cat_id)
    return render(request, 'cats/detail.html', {
        'cat': cat
    })

class CatCreate(CreateView):
    model = Cat
    # fields = ['name', 'breed'] # if model changed, will have ot come back here and update
    fields = '__all__'
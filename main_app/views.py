import os
import uuid
import boto3

from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from .models import Cat, Toy, Photo

from .forms import FeedingForm

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
    feeding_form = FeedingForm()
    current_toys_ids = cat.toys.all().values_list('id')
    available_toys = Toy.objects.exclude(id__in=current_toys_ids)
    return render(request, 'cats/detail.html', {
        'cat': cat,
        'feeding_form': feeding_form,
        'available_toys': available_toys
    })

def add_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.add(toy_id)
    return redirect('detail', cat_id=cat_id)

def remove_toy(request, cat_id, toy_id):
    Cat.objects.get(id=cat_id).toys.remove(toy_id)
    return redirect('detail', cat_id=cat_id)

def add_feeding(request, cat_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.cat_id = cat_id
        new_feeding.save()
    return redirect('detail', cat_id=cat_id)

class CatCreate(CreateView):
    model = Cat
    fields = ['name', 'breed', 'description', 'age']

    def form_valid(self, form):
        form.instance.user = self.request.user # assigned the logged in user (self.request.user)
        return super().form_valid(form) # let the CreateView do its job as usual (saving the object and redirecting)

class CatUpdate(UpdateView):
    model = Cat
    fields = ['breed', 'description', 'age']

class CatDelete(DeleteView):
    model = Cat
    success_url = '/cats/'


# TOY CRUD ###############################################

class ToyList(ListView):
    model = Toy

class ToyDetail(DetailView):
    model = Toy

class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'

class ToyUpdate(UpdateView):
    model = Toy
    fields = '__all__'

class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'

# PHOTO ###################################################

def add_photo(request, cat_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, cat_id=cat_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', cat_id=cat_id)

# SIGNUP ##################################################

def signup(request):
    error_message = ''
    if request.method == 'POST':   
        form = UserCreationForm(request.POST) # this is how we create a 'user' form object that includes the data from the browser
        if form.is_valid():
            user = form.save() # this will add the user to the database
            login(request, user) # automatically log in the new user
            return redirect('index')
        else:
            error_message = 'Invalid sign up. Try again.'

    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

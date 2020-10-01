from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
# from relight.forms.forms import Customer_SignUpForm ,  Shop_SignUpForm

# Create your views here.

def top(request):
   return render(request, 'relight/top.html',{})

def create_aka_before(request):
   return render(request, 'relight/create_aka_before.html',{})

def create_aka_after(request):
   '''if request.method == 'POST':
        form = Customer_SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})'''
   return render(request, 'relight/create_aka_after.html',{})

def cus_login(request):
   return render(request, 'relight/cus_login.html',{})

def shop_login(request):
   return render(request, 'relight/shop_login.html',{})

def cus_profile(request):
   return render(request, 'relight/cus_profile.html',{})

def shop_profile(request):
   return render(request, 'relight/shop_profile.html',{})

def event_index(request):
   return render(request, 'relight/event_index.html',{})

def event_detail(request):
   return render(request, 'relight/event_detail.html',{})

def create_event(request):
   return render(request, 'relight/create_event.html',{})

def shop_video(request):
   return render(request, 'relight/shop_video.html',{})

def cus_video(request):
   return render(request, 'relight/cus_video.html',{})



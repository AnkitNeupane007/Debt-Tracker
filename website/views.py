from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, AddRecordForm
from .models import Records

# Create your views here.
@login_required(login_url='login')
def home(request):
    records = Records.objects.all()
    return render(request, 'home.html', {'records':records})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are logged in!!')
            return redirect('home')
        else:
            messages.error(request, 'Error logging in..')
            return redirect('login')

    if request.user.is_authenticated:
        return redirect('home')
    else:
        return render(request, 'login.html', {})

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    messages.success(request, 'Successfully logged out!!')
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Login after registration
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, 'New account registered successfully!!')
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

    return render(request, 'register.html', {'form': form})

@login_required(login_url='login')
def person_record(request, pk):
    person_record = Records.objects.get(id=pk)
    return render(request, 'record.html', {'person_record': person_record})

@login_required(login_url='login')
def delete_record(request, pk):
    delete_data = Records.objects.get(id=pk)
    messages.success(request, f'Deleted the record of {delete_data.name}')
    delete_data.delete()
    return redirect('home')

@login_required(login_url='login')
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid:
            add_record = form.save()
            messages.success(request, 'New record added')
            return redirect('home')
    return render(request, 'add_record.html', {'form': form})

@login_required(login_url='login')
def user_profile(request):
    return render(request, 'user_profile.html', {})

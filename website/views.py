from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, AddRecordForm
from .models import Records
from django.contrib.auth.models import User
from django.core.mail import send_mail
from crm.settings import EMAIL_HOST_USER

# Create your views here.
@login_required(login_url='login')
def home(request):
    user = request.user
    records = Records.objects.filter(user=user)
    return render(request, 'home.html', {'records': records})

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
    user = request.user
    person_record = Records.objects.get(id=pk, user=user)
    return render(request, 'record.html', {'person_record': person_record})

@login_required(login_url='login')
def delete_record(request, pk):
    user = request.user
    delete_data = Records.objects.get(id=pk, user=user)
    messages.success(request, f'Deleted the record of {delete_data.name}')
    delete_data.delete()
    return redirect('home')

@login_required(login_url='login')
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            add_record = form.save(commit=False)
            add_record.user = request.user
            add_record.save()
            messages.success(request, 'New record added')
            return redirect('home')
    return render(request, 'add_record.html', {'form': form})

@login_required(login_url='login')
def user_profile(request, username):
    if request.user.username != username:
        return redirect('user_profile', username=request.user.username)

    user = get_object_or_404(User, username=username)
    debts = Records.objects.filter(user=user)
    debts = debts.count()
    return render(request, 'user_profile.html', {'user': user, 'debts': debts})

@login_required(login_url='login')
def send_reminder(request, pk):
    user = request.user
    person_record = Records.objects.get(id=pk, user=user)

    formatted_created_at = person_record.created_at.strftime('%Y-%m-%d ')
    send_mail(
        'Reminder',
        f'''Dear {person_record.name},

We hope this message finds you well. It appears that a debt of Rs.{person_record.amount} was extended to you by {user.first_name} {user.last_name}
on {formatted_created_at}.

In the spirit of mutual trust and understanding, we kindly remind you of this commitment. Your timely repayment would greatly assist us in maintaining the financial stability.

Thank you for your attention to this matter.

Warm regards,
DebtTracker Team
''',
        EMAIL_HOST_USER,
        [person_record.email],
        fail_silently=False
        )
    messages.success(request, f'Reminder email sent to {person_record.email}')
    return redirect('home')


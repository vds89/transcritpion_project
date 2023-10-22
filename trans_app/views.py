from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UploadedFile, CustomUser, EmailConfirmation
from .forms import SignupForm
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from allauth.account.views import SignupView
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.core.mail import send_mail

import subprocess
import os


# Create your views here.
# Home page
def index(request):
    return render(request, 'login.html')

@login_required
def upload_file(request):
    if request.method == 'POST' and 'file' in request.FILES:
        uploaded_file = request.FILES['file']
        print('UPLOADED_filename ------------------------> ' + str(uploaded_file))
        instance = UploadedFile(file=uploaded_file)
        instance.save()

        # Call your Python script with the uploaded file as input
        script_path = '/home/vds/Documenti/dev_projects/transcritpion_project/trans_app/scripts/main_tr.py'  # Replace with the actual path to your script
        input_file_path = instance.file.path
        print('UPLOADED_filename path------------------------> ' + input_file_path)
        subprocess.run(['python3', script_path, input_file_path], capture_output=True, text=True)

        # Assuming your script saves the transcript as title.txt in the same directory
        transcript_filename = os.path.join(settings.MEDIA_ROOT, 'uploads', str(uploaded_file) + ".txt")
        print('Transcript_filename ------------------------> ' + transcript_filename)
        if os.path.exists(transcript_filename):
            with open(transcript_filename, 'rb') as f:
                response = HttpResponse(f.read(), content_type='text/plain')
                response['Content-Disposition'] = f'attachment; filename=' + str(uploaded_file) + ".txt"
            return response
        else:
            return HttpResponse('Transcript not found.')
    return render(request, 'upload.html')

'''def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Check if the username or email already exists
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists.')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists.')
            else:
                # Username and email are unique, so save the user
                user = form.save()
                login(request, user)
                messages.success(request, 'User registered successfully.')
                return redirect('login')  # Redirect to a login view
    else:
        print("SIGNUP FAILED !!!!!!")  # Debugging statement
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})
'''

def signup(request):
    return SignupView.as_view()(request)

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print('USERNAME: ' + str(username))
        print('PASSWORD: ' + str(password))
        user = authenticate(request, username=username, password=password)
        print('You are in the login check')
        print('USER: ' + str(user))
        if user is not None:
            login(request, user)
            print('LOGIN OK')
            return redirect('upload_file')  # Redirect to a dashboard or home page
        else:
            # Handle login error
            print('LOGIN FAILED BECAUSE USER is NONE !!!!!!')
            pass  # You can customize the error handling here
    print('OUT of LOGIN !!!!!!')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')


def send_email_confirmation(request, user):
    token = default_token_generator.make_token(user)
    email_confirmation = EmailConfirmation.objects.create(user=user, token=token)
    email_confirmation.save()
    
    current_site = get_current_site(request)
    mail_subject = "Confirm your email"
    message = f"Click the link below to confirm your email:\n"
    message += f"http://{current_site}{reverse('confirm_email', args=[str(email_confirmation.token)])}"
    
    send_mail(mail_subject, message, 'ingegnere31@hotmail.it', [user.email])

def confirm_email(request, token):
    try:
        email_confirmation = EmailConfirmation.objects.get(token=token, is_confirmed=False)
        user = email_confirmation.user
        default_token = default_token_generator.make_token(user)
        if email_confirmation.token == default_token:
            email_confirmation.is_confirmed = True
            email_confirmation.save()
            login(request, user)
            return redirect(reverse('login'))  # Redirect to the user's profile page
    except EmailConfirmation.DoesNotExist:
        # Handle invalid or expired confirmation links
        pass
    return render(request, 'email_confirmation_failed.html')
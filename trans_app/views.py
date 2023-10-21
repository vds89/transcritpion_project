from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UploadedFile
from .forms import SignupForm
from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

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

def signup(request):
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

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print('You are in the login check')
        print(user)
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
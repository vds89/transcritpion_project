from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import UploadedFile
from django.conf import settings
import subprocess
import os

def upload_file(request):
    if request.method == 'POST' and request.FILES['file']:
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
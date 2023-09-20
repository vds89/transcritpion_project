from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import FileUploadForm
from .models import UploadedFile
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404

import os
import subprocess


def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()
            
            # Call your Python script to process the uploaded file here
            processed_file_path = process_file(uploaded_file.file.path)
            
            # Construct the destination path for the processed file in the 'media/processed/' folder
            processed_file_name = os.path.basename(processed_file_path)
            destination_path = os.path.join(settings.MEDIA_ROOT, 'processed', processed_file_name)
            
            # Move the processed file to the 'media/processed/' folder
            os.rename(processed_file_path, destination_path)

            # Store the processed_file_path in the session
            request.session['processed_file_path'] = processed_file_path

            return redirect('download_file', file_id=uploaded_file.id)
    else:
        form = FileUploadForm()
    return render(request, "upload.html", {'form': form})


def download_file(request, file_id):
    # Retrieve the UploadedFile object based on the file_id
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    
    # Retrieve the processed_file_path from the session
    processed_file_path = request.session.get('processed_file_path')
    print('DOWNLOAD FUNC -> processed_file_path -------------> ' + processed_file_path)
    if processed_file_path:
        # Ensure the file exists at the provided path
        if os.path.exists(processed_file_path):
            # Open the processed file using FileResponse and serve it in the browser
            print ('WE ARE HERE ---> ')
            # Open the processed file using FileResponse and serve it in the browser
            with open(processed_file_path, 'rb') as file:
                response = FileResponse(file, content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{os.path.basename(processed_file_path)}"'
                return response
    
    # Handle the case where the processed file is not found
    return HttpResponse("File not found", status=404)



def process_file(file_path):
    # Replace the following line with the actual command to run your Python script
    # Example: subprocess.run(["python", "path/to/your_script.py", file_path]
    print("process_file function --> " + file_path)
    result = subprocess.run(["python3", "/home/vds/Documenti/dev_projects/transcritpion_project/trans_app/scripts/main_tr.py", file_path], capture_output=True, text=True)
    print('Result of prcess_file func --> ' + str(result))
    #result = subprocess.run(["python3", "/home/vds/Documenti/dev_projects/transcritpion_project/trans_app/scripts/example.py", file_path], capture_output=True, text=True)
    
    # Check if the script executed successfully
    if result.returncode == 0:
        print('Pytohn script called correctly')
        processed_file_path = result.stdout.strip()
        print('processed_file_path --------------------> ' + processed_file_path)
        return processed_file_path
    else:
        # Handle script execution error
        raise Exception(f"Script execution failed: {result.stderr}")
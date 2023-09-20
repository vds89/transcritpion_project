import os
from django.conf import settings

# Define the message to be written to the text file
message = "Hello, World!"

# Create the file path for the text file in the media/processed/ folder
file_path = os.path.join(settings.MEDIA_ROOT, 'media/processed/', 'hello.txt')

# Create the directory if it doesn't exist
os.makedirs(os.path.dirname(file_path), exist_ok=True)

# Write the message to the text file
with open(file_path, 'w') as file:
    file.write(message)

print(f"File saved to {file_path}")
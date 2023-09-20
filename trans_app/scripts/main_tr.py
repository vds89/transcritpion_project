import requests
import sys
import os

from api_02 import *

def build_folder_path(base_path, file_name):
    return os.path.join(base_path, file_name)

# Ensure one command-line argument is provided (the folder name)
if len(sys.argv) != 2:
    print("Usage: python script.py <folder_name>")
    sys.exit(1)

# Provide the known base path
base_path = ""

# Extract the folder_name from command-line argument
file_name = sys.argv[1]

# Build the folder path
file_path = build_folder_path(base_path, file_name)

audio_url = upload(file_path)
save_transcript(audio_url, file_path)

#save_transcript_trial(audio_url, file_path)

def builded_path():
    return file_path
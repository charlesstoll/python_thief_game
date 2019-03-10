import os

def record (file_name, seconds):
    bash_command = "arecord -D plughw:1,0 -f S16_LE -c1 -r44100 -d" + str(seconds) + " " + file_name
    os.system(bash_command)
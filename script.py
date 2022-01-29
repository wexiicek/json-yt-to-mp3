from pytube import YouTube
from json import load
import ffmpeg
import os

def main():
    with open('./urls.json') as f:
        urls = load(f)

    dest_directory = "dest"

    try:
        os.mkdir(dest_directory)
    except FileExistsError:
        print("Destination directory already exists.")

    for url in urls:
        video = YouTube(url)
        title = video.title
        print(f"Working on {title}")

        working_file_name = 'in.webm'

        high_quality_audio_stream = video.streams.filter(only_audio=True).order_by('abr').desc().first()
        f = high_quality_audio_stream.download(filename=working_file_name)
        
        process = (
            ffmpeg
            .input(f"./{working_file_name}")
            .output(f"{dest_directory}/{title}.mp3", format='mp3')
            .run()
        )
        if (os.path.exists(working_file_name)):
            os.remove(working_file_name)

if (__name__ == "__main__"):
    main()
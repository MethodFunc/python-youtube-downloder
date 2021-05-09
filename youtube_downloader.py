""" Notice: Must install pytube, ffmpeg-python"""

import pytube
import os
import re
from datetime import datetime
import ffmpeg


def youtube_downloader(url):
    yt = pytube.YouTube(url)
    videos = yt.streams.filter(mime_type="video/mp4").order_by("resolution").desc()

    for n, video in enumerate(videos):
        print(f"{n}: {video}")

    num = int(input("Select Number to Download: "))

    # title_name, audio_file_name
    regex = r"[^A-Za-z0-9가-힣 \-\_\[\]]+"
    res = videos[num].resolution
    title = videos[num].title
    title = re.sub(regex, "", title)
    title = f"{res}_{title}"
    audio_title = f"{title}_audio"

    if os.path.isfile(f"{title}.mp4"):
        if os.path.getsize(f"{title}.mp4") == videos[num].filesize:
            print("Video File is Exist.")
            exit()

    # temp folder create
    if not os.path.isdir("./temp"):
        os.mkdir("./temp")

    # audio codec not include
    print(f"Download start")
    start = datetime.now()

    if not videos[num].includes_audio_track:
        videos[num].download(output_path="./temp", filename=title)
        yt.streams.filter(file_extension="mp4", type="audio")[0].download(output_path="./temp", filename=audio_title)

        # Merge Video & Audio

        video_input = ffmpeg.input(f"./temp/{title}.mp4")
        audio_input = ffmpeg.input(f"./temp/{audio_title}.mp4")
        output = ffmpeg.output(video_input, audio_input, filename=f"./{title}.mp4", vcodec="copy", acodec="copy",
                               f="mp4", )
        ffmpeg.run(output, overwrite_output=True)

        # delete default files & temp folder
        if os.path.isfile(f"./temp/{title}.mp4"):
            os.remove(f"./temp/{title}.mp4")

        if os.path.isfile(f"./temp/{audio_title}.mp4"):
            os.remove(f"./temp/{audio_title}.mp4")

        try:
            if os.path.isdir('./temp'):
                os.rmdir('./temp')
        except:
            for root, dirs, files in os.walk('./temp', topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))

                for name in dirs:
                    os.rmdir(os.path.join(root, name))

            os.rmdir('./temp')

    else:
        # audio codec is include
        videos[num].download()

    print(f"Complete: {datetime.now() - start}s")


if __name__ == "__main__":
    url = "input YouTube url"

    youtube_downloader(url)

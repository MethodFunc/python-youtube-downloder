import os
from typing import ValuesView
import ffmpeg
import re
import time
from pytube import YouTube, Playlist
from pytube.cli import on_progress



def load_youtube(url):
    return YouTube(url, on_progress_callback=on_progress)


def load_playlist(url):
    return Playlist(url)

def stream_videos(stream, fps=None, subtype=None, res=None, types=None, order=None, progressive=None):
    if order:
        return stream.streams.filter(fps=fps, subtype=subtype, res=res, type=types, progressive=progressive).order_by(
            order).desc()
    else:
        return stream.streams.filter(fps=fps, subtype=subtype, res=res, type=types, progressive=progressive)


def youtube_url(res_num, stream, types, save_path="./output"):
    res_list = ["1080p", "720p", "480p", "360p", "240p", "144p"]

    videos = stream_videos(stream, subtype="mp4", res=res_list[res_num], types=types, order="resolution")
    temp = "./temp"
    for video in videos:
        if video.is_progressive:
            index = videos.index(video)
        else:
            index = 0

    if not os.path.isdir(save_path):
        os.mkdir(save_path)
   
    if videos[index].is_progressive:
        title = videos[index].title
        title = f"{res_list[res_num]}_{title}"
        videos[index].download(output_path=save_path, filename=title)

    else:
        if not os.path.isdir(temp):
            os.mkdir(temp)
        regex = r"[^A-Za-z0-9가-힣 \-\_\[\]]+"
        title = videos[index].title
        title = re.sub(regex, "", title)
        title = f"{res_list[res_num]}_{title}"
        audio_title = f"{title}_audio"
        videos[index].download(output_path=temp, filename=title)
        stream.streams.filter(subtype="mp4", type="audio")[0].download(output_path=temp, filename=audio_title)
        time.sleep(1)

        convert_progressive(video=f"{temp}/{title}.mp4", audio=f"{temp}/{audio_title}.mp4", title=title, save_path=save_path)


def youtube_playlist(res_num, stream, types, save_path="./output"):
    if not os.path.isdir(save_path):
        os.mkdir(save_path) 

    folder_title = stream.title

    for num, st in enumerate(stream):
        video = load_youtube(st)
        print()
        print(f"{len(stream)} - {num}: ")
        youtube_url(res_num,  video, types=types, save_path=f"{save_path}/{folder_title}")
        time.sleep(1)


def convert_progressive(video, audio, title, save_path):
    video_input = ffmpeg.input(video)
    audio_input = ffmpeg.input(audio)

    output = ffmpeg.output(video_input, audio_input, filename=f"{save_path}/{title}.mp4", vcodec="copy", acodec="copy",
                           f="mp4")

    ffmpeg.run(output, quiet=True, overwrite_output=True)


def remove_folder(temp):
    for root, dirs, files in os.walk(temp, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))

        for name in dirs:
            os.rmdir(os.path.join(root, name))

    os.rmdir(temp)

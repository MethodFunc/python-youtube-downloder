from os import environb
import subprocess
import time

from platform import platform
from pytube_module import youtube_url, load_youtube, load_playlist, youtube_playlist, remove_folder

if "mac" in platform():
    clear = "clear"
if "window" in platform():
    clear = "cls"

select_0 = ["Youtube Url", "Youtube Playlist"]

while True:
    print("Select youtube url or Playlist")
    for num, sel in enumerate(select_0):
        print(f"[{num}]: {sel}")
    sel0 = int(input("...(9: exit): "))
    subprocess.call(clear)

    if sel0 < 2:
        break

    if sel0 == 9:
        exit()

    if sel0 >= 2:
        print("Wrong Selected")
        time.sleep(1)
        subprocess.call(clear)

res_list = ["1080p", "720p", "480p", "360p", "240p", "144p"]

while True:
    url = input("Input Youtube_url(9: exit): ")

    if url == "9":
        exit()

    try:
        if sel0 == 0:
            stream = load_youtube(url)
        if sel0 == 1:
            stream = load_playlist(url)
        if stream:
            subprocess.call(clear)
            break


    except:
        print("Wrong Youtube URL")
        time.sleep(1)
        subprocess.call(clear)

while True:
    print("Select resolution")
    for num, res in enumerate(res_list):
        print(f"[{num}]: {res}")

    res_select = int(input("...(9: exit): "))
    if res_select < 6:
        break

    if res_select == 9:
        exit()

    if res_select >= 6:
        print("Wrong Number")
        time.sleep(1)
        subprocess.call(clear)
if sel0 == 0:
    youtube_url(res_list[res_select], stream)

if sel0 == 1:
    youtube_playlist(res_list[res_select], stream)

print()
remove_folder(temp="./temp")
print("Download Complete")

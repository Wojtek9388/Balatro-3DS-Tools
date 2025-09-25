import imgui

# Folder Stuffs
import pathlib
import os

from BatchToolRunner import *

def AudioGui():
    imgui.text("Put audiofiles in \"Input\\Audio\".")
    if imgui.button("Compress audio"):
        print("Compressing Audio files...")

        if not os.path.exists("Input\\Audio"):
            os.makedirs("Input\\Audio")
            print("No files in \"Input\\Audio\"\n")
            print("please add audio files (eg. ogg wav mp3 flac) to the newly created folder.")

        FileTypes = ["*.ogg", "*.wav", "*.mp3", "*.flac"]

        AudioFiles = []
        for Extention in FileTypes:
            AudioFiles.extend(pathlib.Path("Input\\Audio").rglob(Extention))

        ### AudioFiles = pathlib.Path("Input\\Audio").rglob("*.ogg") # tripple # is for temporary removal or for easy replacment.

        if AudioFiles:
            for File in AudioFiles:
                print(File.resolve())
                CompressAudio(File.resolve())
        else:
            print("No files in \"Input\\Audio\"")
            print("please add audio files (eg. ogg wav mp3 flac) to the newly created folder.")

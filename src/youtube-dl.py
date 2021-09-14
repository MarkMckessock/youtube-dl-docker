#!/usr/bin/env python

import youtube_dl
import logging
import yaml
import os

from typing import List

DESTINATION_FOLDER = os.getenv("DOWNLOAD_FOLDER","/downloads")
CHANNEL_FILE = os.getenv("CHANNEL_FILE_PATH","/app/channels.yaml")
PLAYLIST_FILE = os.getenv("PLAYLIST_FILE_PATH","/app/playlists.yaml")
ARCHIVE_FILE = os.getenv("ARCHIVE_FILE_PATH","/app/archive.txt")
DOWNLOAD_FORMAT = os.getenv("YOUTUBE_DL_FORMAT","bestvideo+bestaudio[ext=m4a]/mp4")
YOUTUBE_USERNAME = os.getenv("YOUTUBE_USERNAME")
YOUTUBE_PASSWORD = os.getenv("YOUTUBE_PASSWORD")

def download_videos(ids: List[str]) -> None:
    ydl_opts = {
        'outtmpl':'{}/%(uploader)s [%(channel_id)s]/%(title)s [%(id)s].%(ext)s'.format(DESTINATION_FOLDER),
        'username': YOUTUBE_USERNAME,
        'password': YOUTUBE_PASSWORD,
        'writethumbnail': 'true',
        'forcetitle': 'true',
        'ignoreerrors': 'true',
        'download_archive': ARCHIVE_FILE,
        'format': DOWNLOAD_FORMAT,
        'merge_output_format':'mp4',
        'postprocessors': [
            {'key': 'FFmpegMetadata'},
            {'key': 'EmbedThumbnail'},
        ],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(ids)

def load_ids() -> List[str]:
    files = [PLAYLIST_FILE, CHANNEL_FILE]
    ids = []
    for file_path in files:
        if os.path.isfile(file_path):
            with open(file_path, 'r') as fp:
                content = yaml.safe_load(fp)
                if type(content) is list:
                    ids += content
                else:
                    logging.warn(f"File {file_path} is not a valid list of channel/playlist/video ids. Ignoring.")
    return ids

ids = load_ids()
download_videos(ids)
from pathlib import Path

from loguru import logger
from pytube import YouTube
from main import app

from src.file_processor import process_file

class YoutubeHandler():
    _folder_path = Path('data')/'youtube'

    @classmethod
    def handle_youtube_video(cls, txt_file_path_str:str):
        logger.info("Processing youtube video")
        txt_file_path = Path(txt_file_path_str)
        with open(txt_file_path,'r') as f:
            link = f.read()
        txt_file_path.unlink()
        vid = YouTube(link)
        q = vid.streams.filter(file_extension='mp4').first()
        new_path = cls._folder_path
        q.download(new_path)
        process_file.delay(str(new_path / q.default_filename))

@app.task(name='handle_youtube')
def handle_youtube(path:str):
    YoutubeHandler.handle_youtube_video(path)
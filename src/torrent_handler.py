from pathlib import Path
from shutil import move as sh_move, rmtree as sh_rmtree

import torrentp

from main import app
from src.extensions import VIDEO_FILE_EXTENSIONS
from src.file_processor import process_file


class TorrentHandler:
    _folder_path = Path('data') / 'torrent'
    _processing_folder = Path('data') / 'processing'

    @classmethod
    def handle(cls, torrent_path_str: str):
        torrent_path = Path(torrent_path_str)
        torrent_folder_path = cls._folder_path / torrent_path.name
        tf = torrentp.TorrentDownloader(str(torrent_path), str(torrent_folder_path))
        tf.start_download()
        torrent_path.unlink()
        for video in list(torrent_folder_path.glob("*")):
            if video.suffix in VIDEO_FILE_EXTENSIONS:
                new_path = cls._processing_folder / video.name
                sh_move(video,new_path)
                process_file.delay(str(new_path))
                sh_rmtree(torrent_folder_path)
            video.unlink(missing_ok=True)


@app.task(name='handle_torrent')
def handle_torrent(path:str):
    TorrentHandler.handle(path)



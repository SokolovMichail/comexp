from pathlib import Path
from shutil import rmtree as sh_rmtree, move as sh_move

import celery
from loguru import logger

from main import app
from src.extensions import VIDEO_FILE_EXTENSIONS
from src.file_processor import process_file
from src.youtube_handler import handle_youtube
from src.torrent_handler import handle_torrent


class InputProcessor:
    _input_path = Path('data') / 'input'
    _processing_folder = Path('data') / 'processing'

    @classmethod
    def handle_input(cls):
        """
        The input can be provided as a:
        File itself
        .txt file with a youtube link inside
        .torrent file
        """
        logger.info('Starting handle_input func')
        files_in_folder = list(cls._input_path.glob("*"))
        for file in files_in_folder:
            if not file.is_file():
                logger.info("1")
                pass
            else:
                new_path = cls._processing_folder / file.name
                sh_move(file, new_path)
                if file.suffix in VIDEO_FILE_EXTENSIONS:
                    process_file.delay(str(new_path))
                elif file.suffix == '.torrent':
                    handle_torrent.delay(str(new_path))
                elif file.suffix == '.txt':
                    handle_youtube.delay(str(new_path))

@app.task(name='handle_input')
def handle_input():
    InputProcessor().handle_input()
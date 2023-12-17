import subprocess
from pathlib import Path
from loguru import logger
from main import app

class FileProcessor:

    @staticmethod
    def execute_ffmpeg_command(file_path_str:  str):
        if Path(file_path_str).exists():
            try:
                subprocess.call(f"ffmpeg -y -i '{file_path_str}' -f null -",shell=True)
                logger.info(f"Processed file {file_path_str}")
            except:
                logger.error(f"Processing of file {file_path_str} went wrong")
            finally:
                Path(file_path_str).unlink()

        else:
            logger.error(f"No such file {file_path_str}. Aborting process")

@app.task(name='process_file')
def process_file(file_path):
    FileProcessor.execute_ffmpeg_command(file_path)
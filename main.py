from pathlib import Path

from celery import Celery
from kombu import Exchange, Queue

app = Celery('tasks', broker='pyamqp://guest@rabbitmq//')


exchange = Exchange('tasks')

app.conf.task_queues = (
    Queue('input', exchange, routing_key='input'),
    Queue('file', exchange, routing_key='file'),
    Queue('youtube', exchange, routing_key='youtube'),
    Queue('torrent', exchange, routing_key='torrent'),
)
app.conf.task_routes = {
    'handle_input': {'queue': 'input', 'routing_key': 'input'},
    'handle_youtube': {'queue': 'youtube', 'routing_key': 'youtube'},
    'handle_torrent': {'queue': 'torrent', 'routing_key': 'torrent'},
    'process_file': {'queue': 'file', 'routing_key': 'file'},
    #process-images: {'queue' : 'image_chunks', 'routing_key': 'image_chunks'}
}


from src.input_processor import handle_input

@app.on_after_configure.connect
def add_periodic(sender, **kwargs):
    #sender.add_periodic_task(1.0, vee.s(str(Path('dick'))))
    sender.add_periodic_task(10.0, handle_input.s())
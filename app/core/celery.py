from celery import Celery

from app.core.config import settings

app = Celery(
    settings.REDIS_MATCHING_QUEUE,
    broker=f'redis://{settings.REDIS_HOST}:6379/0',
    backend=f'redis://{settings.REDIS_HOST}:6379/1',
    include=["app.services.celery"]
)
app.conf.task_acks_late = True   # Ensures jobs are processed one at a time
app.conf.worker_prefetch_multiplier = 1  # Prevents prefetching multiple jobs
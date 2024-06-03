from celery import Celery

app = Celery('news_crawler',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0',
             include=['tasks'])

app.conf.update(
    result_expires=3600,
    task_annotations={
        '*': {'rate_limit': '10/s'}
    },
    worker_send_task_events=True,
    task_send_sent_event=True,
)


if __name__ == '__main__':
    app.start()

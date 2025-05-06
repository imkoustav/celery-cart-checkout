# from celery import Celery
# from app import create_app

# flask_app = create_app()
# celery = Celery(__name__, broker=flask_app.config['CELERY_BROKER_URL'])
# celery.conf.update(flask_app.config)

# with flask_app.app_context():
#     from app.tasks import *  # Import Celery tasks


from app.tasks import celery

# if __name__ == "__main__":
#     celery.start()

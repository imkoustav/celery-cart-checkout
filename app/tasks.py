# # Define your Celery tasks here
# import time
# from celery import Celery
# from app import create_app, db
# from .models import Checkout, CheckoutStatusEnum

# # Create Celery instance
# celery = Celery(
#     __name__,
#     broker='redis://localhost:6379/0',
#     backend='redis://localhost:6379/0'
# )

# # Bind Flask context to Celery
# app = create_app()
# celery.conf.update(app.config)

# @celery.task()
# def process_checkout(checkout_id):
#     with app.app_context():
#         checkout = Checkout.query.get(checkout_id)
#         if not checkout:
#             return

#         # Update status to Processing
#         checkout.status = CheckoutStatusEnum.processing
#         db.session.commit()

#         start = time.time()

#         # Simulate processing (e.g., payment, discounts)
#         time.sleep(2)

#         # Update status to Completed
#         checkout.status = CheckoutStatusEnum.completed
#         db.session.commit()

#         end = time.time()

#         # Store processing time if needed
#         from .routes import checkout_times
#         if checkout_id in checkout_times:
#             checkout_times[checkout_id] = (checkout_times[checkout_id][0], end)


import os
import time
from celery import Celery
from app import create_app, db
from app.models import Checkout, CheckoutStatusEnum

# Create Flask app
flask_app = create_app()

# Initialize Celery
# celery = Celery(__name__, broker=flask_app.config['CELERY_BROKER_URL'])
# celery.conf.update(flask_app.config)
celery = Celery(__name__)
celery.config_from_object(flask_app.config, namespace="CELERY")

# @celery.task
# def process_checkout(checkout_id):
#     with flask_app.app_context():
#         checkout = Checkout.query.get(checkout_id)
#         if not checkout:
#             print(f"Checkout {checkout_id} not found.")
#             return

#         # Update to 'Processing'
#         checkout.status = CheckoutStatusEnum.processing
#         db.session.commit()

#         # Simulate processing delay
#         time.sleep(2)

#         # Update to 'Completed'
#         checkout.status = CheckoutStatusEnum.completed
#         db.session.commit()
#         print(f"Checkout {checkout_id} marked as completed.")

# @celery.task
# def process_checkout(checkout_id):
#     with flask_app.app_context():
#         checkout = Checkout.query.get(checkout_id)
#         if not checkout:
#             print(f"Checkout {checkout_id} not found.")
#             return

#         # Update to 'Processing'
#         checkout.status = CheckoutStatusEnum.processing
#         db.session.commit()

#         # Simulate varied delay — some will take longer to complete
#         if checkout_id % 2 == 0:
#             time.sleep(5)  # Long delay to simulate pending
#         else:
#             time.sleep(1)  # Quick completion

#         # Update to 'Completed'
#         checkout.status = CheckoutStatusEnum.completed
#         db.session.commit()
#         print(f"Checkout {checkout_id} marked as completed.")


@celery.task
def process_checkout(checkout_id):
    with flask_app.app_context():
        checkout = Checkout.query.get(checkout_id)
        if not checkout:
            print(f"Checkout {checkout_id} not found.")
            return

        # Simulate varied queue delay BEFORE marking as 'Processing'
        if checkout_id % 2 == 0:
            time.sleep(5)  # Simulate staying in 'Pending'
        else:
            time.sleep(1)

        # Now mark as 'Processing'
        checkout.status = CheckoutStatusEnum.processing
        db.session.commit()

        # Simulate actual processing time
        time.sleep(2)

        # Mark as 'Completed'
        checkout.status = CheckoutStatusEnum.completed
        db.session.commit()
        print(f"Checkout {checkout_id} marked as completed.")

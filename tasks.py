from app import celery

@celery.task(bind=True)
def celery_test2(self):
    print("YADA YADA YADA")
    print(f"Received task from 2!: {self}")

@celery.task(bind=True)
def gather_device_data(self):
    print('holla')
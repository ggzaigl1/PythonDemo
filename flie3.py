import time
import itertools

import polling
import requests


def poll_task():
    # Your polling task
    print("Polling task is running")


while True:
    poll_task()
    time.sleep(1)  # Polling interval in seconds

import threading
import keyboard


class Timer:
    def __init__(self, time, func):
        self.thread = threading.Timer(time, func)
        self.thread.daemon = True

    def start(self):
        self.thread.start()



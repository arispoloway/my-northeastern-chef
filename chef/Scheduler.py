import threading
import time


tasks = []


class TimedEvent(object):
    def __init__(self, time, func, args):
        self.time = time
        self.func = func
        self.args = args

    def should_run(self):
        return self.time < time.time()

    def run(self):
        self.func(*self.args)


def schedule_delayed_task(delay, func, args):
    schedule_timed_task(time.time() + delay, func, args)

def schedule_timed_task(time, func, args):
    with threading.Lock():
        tasks.append(TimedEvent(time, func, args))


def run():
    while True:
        with threading.Lock():
            run_tasks = [task for task in tasks if task.should_run()]
            for task in run_tasks:
                task.run()
            for task in run_tasks:
                tasks.remove(task)
        time.sleep(1)










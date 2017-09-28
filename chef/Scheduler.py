import sched
import time


class Scheduler(object):

    scheduler = None

    @staticmethod
    def initialize():
        Scheduler.scheduler = sched.scheduler(time.time, time.sleep)
        Scheduler.keep_alive()

    @staticmethod
    def run():
        Scheduler.scheduler.run()

    @staticmethod
    def keep_alive():
        Scheduler.scheduler.enter(10000, 0, Scheduler.keep_alive, ())

    @staticmethod
    def schedule_delay(delay, func, args):
        Scheduler.scheduler.enter(delay, 0, func, args)

    @staticmethod
    def schedule_time(time, func, args):
        Scheduler.scheduler.enterabs(time, 0, func, args)

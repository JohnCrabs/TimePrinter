import datetime as dt
import warnings
import keyboard
import threading
import time
import sys


class TimePrinter:
    def __init__(self, minutes=10):
        if minutes < 1  or minutes > 180:
            warnings.warn("Minutes out of range (1, 180). Set to default value Minutes = 10!")
            minutes = 10
        self.minutes = minutes
        self.t_start = self.t_start = threading.Thread(target=self._showCurrentDatetimeEachSeconds, daemon=True)
        self.t_key_stop = threading.Thread(target=self._checkStopCondition, daemon=True)
        self.loopTimer = False
        self.loopKey = False
        self._start()

    @staticmethod
    def _getCurrentDatetime():
        return dt.datetime.now()

    def _showCurrentDatetime(self):
        print(self._getCurrentDatetime())

    def _showCurrentDatetimeEachSeconds(self):
        print("Start Timer!")
        while self.loopTimer:
            print(self._getCurrentDatetime())
            time.sleep(self.minutes*60)

    def _checkStopCondition(self):
        while self.loopKey:
            if keyboard.is_pressed('q') or keyboard.is_pressed('esc'):
                self.loopTimer = False
                self.loopKey = False
                self.t_start.join(timeout=0.0)
                print("Stop Timer!")
                sys.exit()

    def _start(self):
        self.loopTimer = True
        self.loopKey = True
        self.t_key_stop.start()
        self.t_start.start()

    def stop(self):
        self.loopTimer = False
        self.loopKey = False
        self.t_start.join(timeout=0.0)
        self.t_key_stop.join(timeout=0.0)

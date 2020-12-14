import threading
import time
import datetime
import warnings
import keyboard


class TimeTimer:
    def __init__(self, minutes=10, target=None):
        if minutes < 1 or minutes > 180:
            warnings.warn("Minutes out of range (1, 180). Set to default value Minutes = 10!")
            minutes = 10
        self.minutes = minutes

        if target is None:
            self.target = self._showTime
        else:
            self.target = target
        self.timer_loop = True
        self.t_timer = threading.Thread(target=self._startTimer,
                                        name="t_timer",
                                        args=(self.minutes*60, self.target),
                                        daemon=False)

        self.t_timer_stop = threading.Thread(target=self._stopTimer,
                                             name="t_timer_stop",
                                             args=(),
                                             daemon=False)

        self.event = threading.Event()

        self.t_timer.start()
        self.t_timer_stop.start()

        self.t_timer.join()
        self.t_timer_stop.join()

    @staticmethod
    def _showTime():
        print("The time is: {}".format(datetime.datetime.now().strftime('%H:%M:%S')))

    def _startTimer(self, delay, target):
        while self.timer_loop:
            try:
                target()
            except ValueError:
                print("Target is not a method!")
            self.event.wait(timeout=delay)

    def _stopTimer(self):
        loop = True
        while loop:
            if keyboard.is_pressed('q') or keyboard.is_pressed('esc'):
                self.timer_loop = False
                self.event.set()
                loop = False
        print("Stop Timer!")


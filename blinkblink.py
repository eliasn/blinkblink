import os
import json
from pathlib import Path
import rumps


APP_CONFIG_DIR = os.path.join(Path.home(), '.local', 'blinkblink')
APP_CONFIG = os.path.join(APP_CONFIG_DIR, 'config.json')


class Alarm:
    def __init__(self, timeout, recurring, trigger_func):
        self.running = False
        self.timeout = timeout
        self.recurring = recurring
        self.trigger_func = trigger_func
        self.left = self.timeout

    def start(self):
        if self.left > 0:
            self.running = True

    def stop(self):
        self.running = False

    def toggle(self):
        if self.running:
            self.stop()
        else:
            self.start()

    def restart(self):
        self.left = self.timeout
        self.running = True

    def tick(self):
        if not self.running:
            return
        self.left -= 1
        if self.left == 0:
            if self.recurring:
                self.left = self.timeout
            else:
                self.running = False
            self.trigger_func(self)
        return self.left


def _pretty(interval: int, unit: bool = True) -> str:
    intervals = [86400, 3600, 60, 1]
    names = ['d', 'h', 'm', 's']
    s = ''
    for i, n in zip(intervals, names):
        name = n if unit else ':'
        if interval >= i:
            s += f'{interval // i}{name}'
            interval %= i
    if not s:
        s = '0'
    if not unit:
        s = s[:-1]
    return s


class BlinkBlinkApp:
    def __init__(self):
        self.config = {
            'interval': 1200,  # 20 min
            'pause': 3600,  # 1 hour
            'reminder': 'Move your eyes away from the screen :)',
        }
        os.makedirs(APP_CONFIG_DIR, exist_ok=True)
        if os.path.isfile(APP_CONFIG):
            config = json.load(open(APP_CONFIG))
            self.config.update(config)
        self.app = rumps.App('blinkblink', '👀')
        self.pause_item = rumps.MenuItem(f'Pause for {_pretty(self.config["pause"])}',
                                         callback=self.pause)
        self.resume_item = rumps.MenuItem('Resume', callback=None)
        self.app.menu = [self.pause_item, self.resume_item]
        self.main_alarm = Alarm(self.config['interval'], True, self.notify)
        self.control_alarm = Alarm(self.config['pause'], False,
                                   lambda _: self.main_alarm.start())
        self.main_alarm.start()
        self.timer = rumps.Timer(self.tick, 1)
        self.timer.start()

    def run(self):
        self.app.run()

    def notify(self, timer):
        self.app.title = '👀'
        rumps.notification(title='blinkblink',
                           subtitle='',
                           message=self.config['reminder'],
                           action_button='Okay')

    def tick(self, sender):
        main_left = self.main_alarm.tick()
        ctrl_left = self.control_alarm.tick()
        if main_left is not None:
            self.app.title = _pretty(main_left, unit=False)
            self.resume_item.title = 'Resume'
        else:
            self.app.title = '👀'
            if ctrl_left is not None:
                self.resume_item.title = f'Resume [auto in {_pretty(ctrl_left)}]'
            else:
                self.resume_item.title = 'Resume'

    def pause(self, sender):
        self.main_alarm.stop()
        self.control_alarm.restart()
        self._toggle_menu_items()

    def resume(self, sender):
        self.control_alarm.stop()
        self.main_alarm.restart()
        self._toggle_menu_items()

    def _toggle_menu_items(self):
        paused = self.control_alarm.running
        self.resume_item.set_callback(self.resume if paused else None)
        self.pause_item.set_callback(None if paused else self.pause)


if __name__ == '__main__':
    app = BlinkBlinkApp()
    app.run()

import rumps


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


class BlinkBlinkApp:
    def __init__(self):
        self.config = {
            'app_name': 'blinkblink',
            'interval': 1200,  # 20 min
            'pause': 'Pause for one hour',
            'resume': 'Resume',
            'message': 'Move your eyes away from the screen :)',
        }
        self.app = rumps.App('blinkblink', '👀')
        self.pause_item = rumps.MenuItem(self.config['pause'],
                                         callback=self.pause)
        self.resume_item = rumps.MenuItem(self.config['resume'],
                                          callback=None)
        self.app.menu = [self.pause_item, self.resume_item]
        self.main_alarm = Alarm(self.config['interval'], True, self.notify)
        self.control_alarm = Alarm(3600, False, lambda _: self.main_alarm.start())
        self.main_alarm.start()
        self.timer = rumps.Timer(self.tick, 1)
        self.timer.start()

    def run(self):
        self.app.run()

    def notify(self, timer):
        self.app.title = '👀'
        rumps.notification(title='blinkblink',
                           subtitle='',
                           message=self.config['message'],
                           action_button='Okay')

    def tick(self, sender):
        left = self.main_alarm.tick()
        self.control_alarm.tick()
        if left is not None:
            min_left = left // 60
            sec_left = left % 60
            self.app.title = f'{min_left:02}:{sec_left:02}'
        else:
            self.app.title = '👀'

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

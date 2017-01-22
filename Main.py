import time

class WODTimer:
    def __init__(self):
        self.count = 0
        self.duration = 0
        self.operation = 1
        self.running = False
        self.mode = 'COUNT_UP'
        self.modes = ['COUNT_UP', 'COUNT_DOWN', 'INTERVAL', 'TABATA', 'FTG']
        self.brightness = 1
        self.ten_seconds_state = False
        self.time_format_state = False
        self.voice_toggle_state = False
        self.interval = 1
        self.interval_total = 8
        self.interval_length = 0
        self.rest = False
        self.rest_length = 10

    def set_mode(self, mode):
        self.mode = mode

    def set_duration(self, duration):
        self.duration = duration

    def set_interval_total(self, total):
        self.interval_total = total

    def set_interval_length(self, length):
        self.interval_length = length

    def reset(self):
        return False

    def exit(self):
        return False

    def toggle_time_format(self):
        return False

    def toggle_voice(self):
        return False

    def toggle_ten_seconds(self):
        return False

    def toggle_normal_clock(self):
        return False

    def update_time(self):
        self.count += self.operation

    def print_time(self):
        minutes, secs = divmod(self.count, 60)
        time_format = '{:02d}:{:02d}'.format(minutes, secs)
        if self.mode == 'INTERVAL':
            time_format = 'INT ' + str(self.interval) + ' ' + time_format
        if self.mode == 'TABATA':
            if self.rest:
                time_format = 'REST' + ' ' + time_format
            else:
                time_format = 'RD' + str(self.interval) + ' ' + time_format
        print(time_format, end='\r')

    def check_completed(self):
        if self.mode == 'COUNT_DOWN':
            if self.count == 0:
                self.running = False
        if self.mode == 'COUNT_UP':
            if self.count == self.duration:
                self.running = False
        if self.mode == 'INTERVAL':
            if self.count == self.interval_length:
                self.count = 0
                self.interval += 1
                if self.interval == self.interval_total + 1:
                    self.running = False
        if self.mode == 'TABATA':
            if self.rest:
                if self.count == self.rest_length:
                    self.rest = False
                    self.count = 0
                    self.interval += 1
            if self.count == self.interval_length:
                self.rest = True
                self.count = 0
            if self.interval == self.interval_total + 1:
                self.running = False

    def count_down(self):
        self.operation = -1

    def count_up(self):
        self.operation = 1

    def run_loop(self):
        while self.running:
            self.update_time()
            self.print_time()
            self.check_completed()
            time.sleep(1)

    def start(self):
        if self.mode == 'COUNT_DOWN':
            self.count = self.duration
            self.count_down()
        if self.mode == 'COUNT_UP':
            self.count = 0
            self.count_up()
        if self.mode == 'TABATA':
            self.count_up()
            self.interval_length = 20
            self.rest_length = 10
            self.rest = False
        self.running = True
        self.run_loop()

timer = WODTimer()

# timer.set_mode('COUNT_UP')
# timer.set_duration(10)
# timer.start()
#
# timer.set_mode('COUNT_DOWN')
# timer.set_duration(10)
# timer.start()

# timer.set_mode('INTERVAL')
# timer.set_interval_total(4)
# timer.set_interval_length(5)
# timer.start()

timer.set_mode('TABATA')
timer.start()
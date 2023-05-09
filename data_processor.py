import time
import threading
import keyboard
import numpy as np
from abc import abstractmethod

import utils
from sensors import Anemometer, Thermometer, RainfallDetector, RainGauge, VisibilityMeter


class RainProcessor:
    """
    Lượng mưa tích tụ trong 1 giờ
    Lượng mưa tích tụ từ thời điểm bắt đầu mưa
    Lượng mưa tức thời mỗi phút
    """

    def __init__(self, rain_gauge: RainGauge,
                 rain_detector: RainfallDetector):
        self.rain_gauge = rain_gauge
        self.rain_detector = rain_detector

        self.dict = {}
        self.rain_perm = 0
        self.rain_perh = 0
        self.rain_cum = 0

        self.reset_perm()
        self.reset_perh()

    def reset_perm(self):
        utils.Timer(10, self.reset_perm).start()

        self.dict['rain_per_min'] = self.rain_perm
        self.rain_perm = 0

    def reset_perh(self):
        utils.Timer(30, self.reset_perh).start()

        self.dict['rain_per_hour'] = self.rain_perh
        self.rain_perh = 0

    def _process(self):
        if self.rain_detector.is_raining():
            if self.rain_gauge.is_full():
                self.rain_perm += 0.5
                self.rain_perh += 0.5
                self.rain_cum += 0.5
                self.dict['rain_cumulative'] = self.rain_cum
        else:
            self.dict['rain_cumulative'] = self.rain_cum
            self.rain_cum = 0

    def update(self):
        self._process()
        self.rain_gauge.update()
        self.rain_detector.update()

    def get(self):
        return self.dict


class TemperatureProcessor:
    """
    Nhiệt độ tức thời mỗi phút
    """

    def __init__(self, thermometer: Thermometer):
        self.thermometer = thermometer

    def update(self):
        self.thermometer.update()

    def get(self):
        return {'temperature': self.thermometer.data}


class WindProcessor:
    """
    Tốc độ gió tối thiểu & tối đa mỗi phút
    Hướng gió tại tốc độ gió tối thiểu & tối đa
    """

    def __init__(self, anemometer: Anemometer):
        self.anemometer = anemometer

        self.speed_min = float('inf')
        self.speed_max = float('-inf')
        self.dir_atMin = 0
        self.dir_atMax = 0
        self.dict = {}

    def reset_perm(self):
        thread = threading.Timer(60, self.reset_perm)
        thread.daemon = True
        thread.start()

        self.dict = {'wind_speed_max': self.speed_max,
                     'wind_speed_min': self.speed_min,
                     'wind_dir_atMax': self.dir_atMax,
                     'wind_dir_atMin': self.dir_atMin}
        self.speed_min = float('inf')
        self.speed_max = float('-inf')

    def _process(self):
        speed, direction = self.anemometer.data

        if speed > self.speed_max:
            self.speed_max = speed
            self.dir_atMax = direction

        if speed < self.speed_min:
            self.speed_min = speed
            self.dir_atMin = direction

    def update(self):
        self._process()
        self.anemometer.update()

    def get(self):
        return self.dict


class VisibilityProcessor:
    """
    Giá trị tầm nhìn tối thiểu & tối đa mỗi phút
    """

    def __init__(self, visibility_meter: VisibilityMeter):
        self.visibility_meter = visibility_meter

        self.dict = {}
        self.min = float('inf')
        self.max = float('-inf')

    def reset_perm(self):
        utils.Timer(60, self.reset_perm).start()

        self.dict = {'visibility_max': self.max,
                     'visibility_min': self.min}
        self.min = float('inf')
        self.max = float('-inf')

    def _process(self):
        if self.visibility_meter.data > self.max:
            self.max = self.visibility_meter.data
        if self.visibility_meter.data < self.min:
            self.min = self.visibility_meter.data

    def update(self):
        self._process()
        self.visibility_meter.update()

    def get(self):
        return self.dict


def get_data(procs: list):
    data_dict = {}

    for proc in procs:
        data_dict.update(proc.get())
    return data_dict


if __name__ == '__main__':
    rain_gauge = RainGauge()
    rain_detector = RainfallDetector()
    thermometer = Thermometer()

    rain_processor = RainProcessor(rain_gauge, rain_detector)
    temperature_processor = TemperatureProcessor(thermometer)

    procs = [rain_processor, temperature_processor]

    while True:
        datalogger = get_data(procs)
        print(datalogger)

        for proc in procs:
            proc.update()

        time.sleep(1)
        if keyboard.is_pressed('q'):
            break

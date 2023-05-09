from abc import abstractmethod
import random


temperature = 0
wind_speed = 0


class BaseSensor:
    @abstractmethod
    def is_error(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def is_controlled(self):
        # Điều khiển thời tiết
        pass


# Nhiệt kế
class Thermometer(BaseSensor):
    operating_range = {'min': 0.0, 'max': 70.0}

    def __init__(self):
        self.temperature = 30.0

    @property
    def data(self):
        return round(self.temperature, 1)

    def update(self):
        self.temperature += random.uniform(-2, 2)

    def is_error(self):
        return not self.operating_range['min'] <= self.temperature <= self.operating_range['max']

    def is_controlled(self):
        pass


# Máy đo gió
class Anemometer(BaseSensor):
    global temperature

    speed_range = {'min': 0.4, 'max': 70.0}
    dir_range = {'min': 0.0, 'max': 360.0}
    operating_range = {'min': 0.0, 'max': 50.0}

    def __init__(self):
        self.wind_speed = 30.
        self.wind_dir = 180.
        self.temperature = temperature

    @property
    def data(self):
        return [round(self.wind_speed, 1), round(self.wind_dir, 1)]

    def update(self):
        self.wind_speed += random.uniform(-self.speed_range['max'] / 20, self.speed_range['max'] / 20)
        self.wind_dir += random.uniform(-self.dir_range['max'] / 20, self.dir_range['max'] / 20)

        self.temperature = temperature

    def is_error(self):
        return not self.speed_range['min'] <= self.wind_speed <= self.speed_range['max'] or \
               not self.dir_range['min'] <= self.wind_dir <= self.dir_range['max'] or \
               not self.operating_range['min'] <= self.temperature <= self.operating_range['max']

    def is_controlled(self):
        pass


# Bình đo lượng mưa
class RainGauge(BaseSensor):
    global temperature

    volume_range = {'min': 0.0, 'max': 0.5}
    operating_range = {'min': 0.0, 'max': 50.0}

    def __init__(self):
        self.current_volume = 0
        self.temperature = temperature

    # Gửi một xung mỗi khi lượng mưa đạt 0.5mm
    def is_full(self):
        if self.current_volume >= self.volume_range['max']:
            self.current_volume = 0
            return True

    @property
    def data(self):
        return round(self.current_volume, 1)

    def update(self):
        self.current_volume += random.uniform(0, self.volume_range['max']/20)
        self.temperature = temperature

    def is_error(self):
        return not self.operating_range['min'] <= self.temperature <= self.operating_range['max']

    def is_controlled(self):
        pass


# Máy phát hiện lượng mưa
class RainfallDetector(BaseSensor):
    global temperature

    operating_range = {'min': 0.0, 'max': 50.0}

    def __init__(self):
        self._is_raining = False
        self.temperature = temperature

    def is_raining(self):
        return True

    def update(self):
        self._is_raining = random.choice([True, False])
        self.temperature = temperature

    def is_error(self):
        return not self.operating_range['min'] <= self.temperature <= self.operating_range['max']

    def is_controlled(self):
        pass


# Máy đo tầm nhìn
class VisibilityMeter(BaseSensor):
    global temperature, wind_speed

    visibility_range = {'min': 10, 'max': 1000}
    operating_range = {'min': 0.0, 'max': 50.0}
    wind_limit = 50

    def __init__(self):
        self.visibility = 500
        self.temperature = temperature

    @property
    def data(self):
        return self.visibility

    def update(self):
        self.visibility += random.randrange(-self.visibility_range['max'], self.visibility_range['max'])
        self.temperature = temperature

    def is_error(self):
        return not self.operating_range['min'] <= self.temperature <= self.operating_range['max'] or \
               not self.visibility_range['min'] <= self.visibility <= self.visibility_range['max'] or \
               wind_speed > 50

    def is_controlled(self):
        pass




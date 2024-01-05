#!/usr/bin/python3

from sense_hat import SenseHat

humid_pixel = [0, 40, 220]
temp_pixel = [240, 40, 0]
off_pixel = [0, 0, 0]
max_humid = 100.0
max_temp = 40.0

class HumidTempGauge:
    def __init__(self, sense=None):
        if sense is None:
            self.sense = SenseHat()
            self.sense.clear()
        else:
            self.sense = sense

    def main_loop(self):
        humidity = self.sense.get_humidity()
        humidity = min(round(humidity, 1), max_humid)
        temp = self.sense.get_temperature()
        temp = min(round(temp, 1), max_temp)

        # print("humidity: {}, temp: {}".format(humidity, temp))

        pixels = []

        # humidity in first 32 pixels
        on_count = int((32 / max_humid) * humidity)
        off_count = 32 - on_count
        pixels.extend([humid_pixel] * on_count)
        pixels.extend([off_pixel] * off_count)

        # temperature in next 32 pixels
        on_count = int((32 / max_temp) * temp)
        off_count = 32 - on_count
        pixels.extend([temp_pixel] * on_count)
        pixels.extend([off_pixel] * off_count)

        self.sense.set_pixels(pixels)

    def finish(self):
        self.sense.clear()

if __name__ == "__main__":
    hg = HumidTempGauge()
    try:
        while True:
            hg.main_loop()
    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        pass
    finally:
        hg.finish()

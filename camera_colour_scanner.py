import time
import threading
import numpy as np
import picamera
import picamera.array


class CameraColourScanner:
    def __init__(self, resolution=(64, 64), interval=1.0):
        self.resolution = resolution
        self.interval = interval
        self.latest_color = (0, 0, 0)
        self.running = False
        self._thread = None

    def _worker(self):
        """The actual background loop."""
        with picamera.PiCamera() as camera:
            camera.resolution = self.resolution
            # Allow sensor to settle
            time.sleep(2)

            with picamera.array.PiRGBArray(camera, size=self.resolution) as stream:
                while self.running:
                    camera.capture(stream, format="rgb", use_video_port=True)

                    # Compute average RGB
                    avg = np.mean(stream.array, axis=(0, 1))
                    self.latest_color = tuple(avg.astype(int))

                    # Reset stream for next frame
                    stream.seek(0)
                    stream.truncate()

                    time.sleep(self.interval)

    def start(self):
        """Starts the background thread."""
        if not self.running:
            self.running = True
            self._thread = threading.Thread(target=self._worker, daemon=True)
            self._thread.start()

    def stop(self):
        """Stops the loop (the thread will exit safely)."""
        self.running = False
        if self._thread:
            self._thread.join()

    @property
    def color(self):
        """Easy access to the most recent value."""
        return self.latest_color

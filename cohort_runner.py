from contextlib import contextmanager
import importlib.util
import os
import threading
from base_runner import BaseRunner
from sense_hat import SenseHat
import time


class CancelExecution(Exception):
    pass


class MockColorSensor(tuple):
    """A tuple that pretends to be a hardware sensor object."""

    def __new__(cls, r, g, b):
        # Create the tuple (R, G, B)
        return super(MockColorSensor, cls).__new__(cls, (r, g, b))

    def __init__(self, r, g, b):
        self.red = r
        self.green = g
        self.blue = b

        # Dummy attributes for the setup calls
        self.gain = 60
        self.integration_cycles = 64
        self.integration_time = 2.4


@contextmanager
def cohort_env_mock(runner):
    """
    Context manager to safely inject and cleanup mocks
    for the student execution environment.
    """
    # Store original functions
    orig_sleep = time.sleep
    orig_show_message = SenseHat.show_message
    current_thread = threading.current_thread()

    # Define the 'Interruptible' versions
    def mocked_sleep(seconds):
        if threading.current_thread() == current_thread:
            end_time = time.time() + seconds
            while time.time() < end_time:
                if runner.stop_requested:
                    raise CancelExecution("Interrupted")
                # Sleep in tiny bursts so we check the flag frequently
                orig_sleep(0.05)
        else:
            orig_sleep(seconds)

    def mocked_show_message(instance, *args, **kwargs):
        if runner.stop_requested:
            raise CancelExecution("Interrupted")
        return orig_show_message(instance, *args, **kwargs)

    # Apply the patches
    time.sleep = mocked_sleep
    SenseHat.show_message = mocked_show_message

    # Force the color property as well
    SenseHat.colour = property(
        lambda inst: MockColorSensor(*runner.scanner.latest_color)
    )
    SenseHat.color = SenseHat.colour

    try:
        yield  # This is where the student code executes
    finally:
        # Cleanup: Restore original functions no matter what happens
        time.sleep = orig_sleep
        SenseHat.show_message = orig_show_message
        # Remove the added properties
        del SenseHat.colour
        del SenseHat.color


class CohortRunner(BaseRunner):
    def __init__(self, camera_colour_scanner, cohort_dir, student_path):
        self.scanner = camera_colour_scanner
        self.cohort_dir = cohort_dir
        self.student_path = student_path
        self.module_path = os.path.join(cohort_dir, student_path)
        self.thread = None
        self.stop_requested = False

    def _check_cancel(self, *args, **kwargs):
        """Internal check to see if we should bail out."""
        if self.stop_requested:
            raise CancelExecution(f"Stopping module {self.student_path}")

    def _run_with_mock(self):
        """Execute the student module in a cancellable way while mocking the SenseHat color."""
        # dynamically load the cohort module
        try:
            with cohort_env_mock(self):
                spec = importlib.util.spec_from_file_location(
                    "cohort_module", self.module_path
                )
                if spec and spec.loader:
                    print(f"starting student module {self.student_path}...")
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)
                else:
                    print(f"Failed to load student module {self.student_path}")
        except CancelExecution:
            pass
        except Exception as e:
            print(f"Error in student module {self.student_path}: {e}")
        finally:
            self.stop_requested = False
            self.thread = None

    def main_loop(self):
        if not self.thread:
            self.stop_requested = False
            self.scanner.start()
            self.thread = threading.Thread(target=self._run_with_mock, daemon=True)
            self.thread.start()

    def stop(self):
        my_thread = self.thread
        if my_thread and my_thread.is_alive():
            print(f"Stopping student module {self.student_path}...")
            self.stop_requested = True
            my_thread.join()
            self.scanner.stop()

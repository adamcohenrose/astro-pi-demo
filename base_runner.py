from abc import ABC, abstractmethod


class BaseRunner(ABC):
    @abstractmethod
    def main_loop(self):
        pass

    @abstractmethod
    def stop(self):
        pass

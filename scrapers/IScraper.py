from abc import ABC, abstractmethod


class IScraper(ABC):

    @abstractmethod
    def getData(self, limit):
        pass

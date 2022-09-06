import abc


class Filter(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def apply(self, image):
        raise NotImplementedError()

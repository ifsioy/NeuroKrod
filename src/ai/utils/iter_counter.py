

class IterCounter:
    counter = 0

    @staticmethod
    def increment():
        IterCounter.counter += 1
        return IterCounter.counter

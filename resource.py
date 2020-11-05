import random
import re

from threading import Timer


class Resource:
    def __init__(self, on_ready_callback):
        Timer(random.random() * 0.8 + 0.2, lambda: on_ready_callback(self.value)).start()

    @property
    def value(self):
        if not hasattr(self, '_value'):
            self._value = re.sub('x', lambda _: '{:x}'.format(random.randint(0, 15)), 'xxxxxxxxxxxxxxxx')

        return self._value

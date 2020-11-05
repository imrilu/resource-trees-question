import unittest

from threading import Event

from resource import Resource


class ResourceTestCase(unittest.TestCase):
    def test_become_ready(self):
        event = Event()
        def on_ready(value):
            nonlocal event
            event.set()

        res = Resource(on_ready)
        
        self.assertFalse(event.is_set(), 'resource should not be ready')
        self.assertTrue(event.wait(1), 'resource should be ready')

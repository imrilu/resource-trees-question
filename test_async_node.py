import unittest

from threading import Event
from time import sleep

from async_node import AsyncNode as Node


class AsyncNodeTestCase(unittest.TestCase):
    def test_when_ready(self):
        event = Event()
        def on_ready():
            nonlocal event
            event.set()

        node = Node()
        node.when_ready(on_ready)
        
        self.assertTrue(event.wait(1), 'when_ready() not called')
        self.assertTrue(node.is_ready(), 'not ready yet')

    def test_when_ready_with_complex_hierarchy(self):
        a = Node()
        b = Node()
        a.add_child(b)
        
        c = Node()
        a.add_child(c)

        d = Node()
        a.add_child(d)

        e = Node()
        d.add_child(e)
        
        event = Event()
        def on_ready():
            nonlocal event
            event.set()

        a.when_ready(on_ready)

        self.assertFalse(event.is_set(), 'a should not be ready')
        
        self.assertTrue(event.wait(1), 'a.when_ready() not called')
        self.assertTrue(a.is_ready(), 'a should be ready')
        self.assertTrue(b.is_ready(), 'b should be ready')
        self.assertTrue(c.is_ready(), 'c should be ready')
        self.assertTrue(d.is_ready(), 'd should be ready')
        self.assertTrue(e.is_ready(), 'e should be ready')

    def test_add_child_after_when_ready(self):
        a = Node()
        b = Node()
        a.add_child(b)
        
        c = Node()
        a.add_child(c)

        d = Node()
        a.add_child(d)

        self.assertFalse(a.is_ready(), 'a should not be ready yet')
        
        event = Event()
        def on_ready():
            nonlocal event
            event.set()

        a.when_ready(on_ready)

        self.assertTrue(event.wait(1), 'a.when_ready() not called')
        self.assertTrue(a.is_ready(), 'a should be ready when the callback for when_ready() was called')
        self.assertTrue(b.is_ready(), 'b should be ready if a is ready')
        self.assertTrue(c.is_ready(), 'c should be ready if a is ready')
        self.assertTrue(d.is_ready(), 'd should be ready if a is ready')

        e = Node()
        d.add_child(e)

        f = Node()
        d.add_child(f)

        self.assertFalse(d.is_ready(), 'd should not be ready after e was added')
        self.assertFalse(a.is_ready(), 'a should not be ready after e was added')

        event.clear()
        a.when_ready(on_ready)

        self.assertTrue(event.wait(1), 'a.when_ready() not called')
        self.assertTrue(e.is_ready(), 'e should be ready if a is ready')

    def test_remove_child_after_when_ready(self):
        a = Node()
        
        b = Node()

        c = Node()
        b.add_child(c)
        
        self.assertFalse(a.is_ready(), 'a should not be ready yet')
        self.assertFalse(b.is_ready(), 'b should not be ready yet')
                
        event = Event()
        def on_ready():
            nonlocal event
            event.set()
        
        b.when_ready(on_ready)

        event.wait(1)

        a.add_child(b)

        d = Node()
        b.add_child(d)
    
        self.assertTrue(c.is_ready(), 'c should not be affected after d was added')
        self.assertFalse(b.is_ready(), 'b should not be ready after d was added')
        self.assertFalse(a.is_ready(), 'a should not be ready after d was added')

        event.clear()
        a.when_ready(on_ready)

        sleep(0.1) # not enough time for d to become ready

        b.remove_child(d) # remove d *before* it had a chance to become ready

        self.assertTrue(a.is_ready(), 'a should be ready after d was removed')
        self.assertFalse(d.is_ready(), 'd should not be ready yet when a becomes ready')

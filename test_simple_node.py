import unittest

from time import sleep

from simple_node import SimpleNode as Node


class SimpleNodeTestCase(unittest.TestCase):
    def test_is_ready(self):
        node = Node()
        
        self.assertFalse(node.is_ready(), 'ready too soon')
        
        sleep(1)
        
        self.assertTrue(node.is_ready(), 'not ready yet')

    def test_is_ready_after_add_child_and_remove_child(self):
        a = Node()
        
        sleep(1)

        self.assertTrue(a.is_ready(), 'a should be ready')
        
        b = Node()
        a.add_child(b)
        
        self.assertFalse(a.is_ready(), 'b should not be ready')
        self.assertFalse(b.is_ready(), 'a should not be ready (due to b addition)')
        
        a.remove_child(b)
        
        self.assertTrue(a.is_ready(), 'a should be ready again (due to b removal)')

    def test_is_ready_with_complex_hierarchy(self):
        a = Node()
        b = Node()
        a.add_child(b)
        
        c = Node()
        a.add_child(c)

        d = Node()
        a.add_child(d)

        e = Node()
        d.add_child(e)
        
        self.assertFalse(a.is_ready(), 'a should not be ready')
        self.assertFalse(b.is_ready(), 'b should not be ready')
        self.assertFalse(c.is_ready(), 'c should not be ready')
        self.assertFalse(d.is_ready(), 'd should not be ready')
        self.assertFalse(e.is_ready(), 'e should not be ready')
            
        sleep(1)
        
        self.assertTrue(a.is_ready(), 'a should be ready')
        self.assertTrue(b.is_ready(), 'b should be ready')
        self.assertTrue(c.is_ready(), 'c should be ready')
        self.assertTrue(d.is_ready(), 'd should be ready')
        self.assertTrue(e.is_ready(), 'e should be ready')
        
        f = Node()
        d.add_child(f)
        
        self.assertFalse(f.is_ready(), 'f should not be ready')
        self.assertFalse(d.is_ready(), 'd should not be ready (direct)')
        self.assertFalse(a.is_ready(), 'a should not be ready (indirect)')
        
        sleep(1)
        
        self.assertTrue(f.is_ready(), 'f should be ready')
        self.assertTrue(d.is_ready(), 'd should be ready (direct)')
        self.assertTrue(a.is_ready(), 'a should be ready (indirect)')

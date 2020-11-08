from simple_node import SimpleNode


class AsyncNode(SimpleNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = None
        self.callback = lambda: None

    def add_child(self, child):
        super().add_child(child)
        child.add_parent(self)
        self.is_ready()

    def remove_child(self, child):
        super().remove_child(child)
        self.is_ready()

    def notify_parent(self, ready):
        if self.parent:
            if ready:
                self.parent.remove_child(self)
            else:
                self.parent.add_child(self)

    def add_parent(self, parent):
        if parent:
            self.parent = parent

    def on_resource_ready(self, value):
        self.resource_ready = True
        self.is_ready()

    def when_ready(self, callback):
        '''
        takes a callback to call when the resources of this node and its subtree all become ready, returns immediately

        Args:
            callback (function): will be called when all resources become ready
        '''
        self.callback = callback
        self.is_ready()

    def is_ready(self):
        if not self.nodes and self.resource_ready:
            self.callback()
            self.notify_parent(True)
            return True
        else:
            self.notify_parent(False)
            return False

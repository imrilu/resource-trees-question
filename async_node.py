from simple_node import SimpleNode


class AsyncNode(SimpleNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = None
        self.callback = lambda: None
        self.ready_nodes = list()

    def add_child(self, child):
        super().add_child(child)
        child.add_parent(self)
        self.is_ready()

    def remove_child(self, child):
        super().remove_child(child)
        self.is_ready()

    def add_ready_child(self, child):
        if child not in self.ready_nodes:
            self.ready_nodes.append(child)
            self.is_ready()

    def remove_ready_child(self, child):
        if child in self.ready_nodes:
            self.ready_nodes.remove(child)
            self.is_ready()

    def notify_parent(self, ready):
        if self.parent:
            if ready:
                self.parent.add_ready_child(self)
            else:
                self.parent.remove_ready_child(self)

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
        if not set(self.nodes).difference(self.ready_nodes) and self.resource_ready:
            self.callback()
            self.notify_parent(True)
            return True
        else:
            self.notify_parent(False)
            return False

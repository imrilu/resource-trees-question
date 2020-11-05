from resource import Resource


class SimpleNode:
    def __init__(self, name=""):
        self.resource_ready = False
        self.res = Resource(self.on_resource_ready)
        self.nodes = list()
        self.name = name

    def on_resource_ready(self, value):
        '''
        an event handler called when the resource becomes ready, should not be called directly

        Args:
            value (str): the resource payload (can be left unused for the scope of the assignment)
        '''
        self.resource_ready = True

    def add_child(self, child):
        '''
        adds child node as a child of this node

        Args:
            child (SimpleNode): the child to add
        '''
        if child not in self.nodes:
            self.nodes.append(child)

    def remove_child(self, child):
        '''
        removes an existing child from this node

        Args:
            child (SimpleNode): the child to add
        '''
        if child in self.nodes:
            self.nodes.remove(child)

    def is_ready(self):
        '''
        checks whether the resources of this node and its subtree are all ready

        Returns:
            bool: are all resources ready
        '''
        if self.resource_ready is False:
            return False
        for node in self.nodes:
            if not node.is_ready():
                return False
        return True

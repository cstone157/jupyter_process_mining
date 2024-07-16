## The Nodes of our trees, if no parent is passed
##     then we will assume that this is the top
##     level of a tree.
## Depth == 0, means it is top level of a tree
class Node:
    ## Constructor
    ## Parameters:
    ##     parent (optional), Node object
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.depth = 0
        ## Check if we have a parent, then set our depth to parent.depth + 1
        if self.parent is not None:
            self.depth = self.parent.depth + 1
        ## A dictionary of children (use the name of the node, as our key
        self.children = {}

    ## updateChildren
    ## Parameter:
    ##     name, string of the name of our children
    def updateChildren(self, name):
        if name in self.children:
            self.children[name] = Node(name, parent=self)
            
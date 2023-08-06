from hashlib import sha256

hash_function = sha256


class Node(object):
    """Each node has references to left and right child nodes, parent, and sibling.
    It can also be aware of whether it is on the left or right hand side. data is hashed
    automatically by default, but does not have to be, if prehashed param is set to False.
    """
    def __init__(self, data, prehashed=False):
        if prehashed:
            self.val = data
        else:
            self.val = hash_function(data).digest()
        self.l = None
        self.r = None
        self.p = None
        self.sib = None
        self.side = None

    def __repr__(self):
        return "Val: <" + str(self.val.encode('hex')) + ">"


class MerkleTree(object):
    """A Merkle tree implementation.  Added values are stored in a list until the tree is built.
    A list of data elements for Node values can be optionally supplied.  Data supplied to the
    constructor is hashed by default, but this can be overridden by providing prehashed=False
    in which case, node values should be supplied in hex format.
    """
    def __init__(self, leaves=[], prehashed=False):
        if prehashed:
            self.leaves = [Node(leaf.decode('hex'), prehashed=True) for leaf in leaves]
        else:
            self.leaves = [Node(leaf) for leaf in leaves]
        self.root = None

    def __eq__(self, obj):
        return (self.root.val == obj.root.val) and (self.__class__ == obj.__class__)

    def add(self, data):
        """Add a Node to the tree, providing data, which is hashed automatically
        """
        self.leaves.append(Node(data))

    def add_hash(self, value):
        """Add a Node based on a precomputed hash value, hex format required/assumed.
        """
        self.leaves.append(Node(value.decode('hex'), prehashed=True))

    def clear(self):
        """Releases the Merkle root, and node references are garbage collected
        """
        self.root = None

    def build(self):
        """Calculate the merkle root and make references between nodes in the tree.
        """
        if not self.leaves:
            raise AssertionError('No leaves')
        layer = self.leaves[::]
        while 1:
            layer = self._build(layer)
            if len(layer) == 1:
                self.root = layer[0]
                break
        return self.root.val.encode('hex')

    def _build(self, leaves):
        """Private helper function to create the next aggregation level and put all references in place
        """
        new, odd = [], None
        # ensure even number of leaves
        if len(leaves) % 2 == 1:
            odd = leaves.pop(-1)
        for i in range(0, len(leaves), 2):
            newnode = Node(leaves[i].val + leaves[i + 1].val)
            newnode.l, newnode.r = leaves[i], leaves[i + 1]
            leaves[i].side, leaves[i + 1].side, leaves[i].p, leaves[i + 1].p = 'L', 'R', newnode, newnode
            leaves[i].sib, leaves[i + 1].sib = leaves[i + 1], leaves[i]
            new.append(newnode)
        if odd:
            new.append(odd)
        return new

    def get_chain(self, index):
        """Assemble and return the chain leading from a given node to the merkle root of this tree
        """
        chain = []
        this = self.leaves[index]
        chain.append((this.val, 'SELF'))
        while 1:
            if not this.p:
                chain.append((this.val, 'ROOT'))
                break
            else:
                chain.append((this.sib.val, this.sib.side))
                this = this.p
        return chain

    def get_all_chains(self):
        """Assemble and return chains for all nodes to the merkle root
        """
        return [self.get_chain(i) for i in range(len(self.leaves))]

    def get_hex_chain(self, index):
        """Assemble and return the chain leading from a given node to the merkle root of this tree
        with hash values in hex form
        """
        return [(i[0].encode('hex'), i[1]) for i in self.get_chain(index)]

    def get_all_hex_chains(self):
        """Assemble and return chains for all nodes to the merkle root, in hex form
        """
        return [[(i[0].encode('hex'), i[1]) for i in j] for j in self.get_all_chains()]


def check_chain(chain):
    """Verify a presented merkle chain to see if the Merkle root can be reproduced.
    """
    link = chain[0][0]
    for i in range(1, len(chain) - 1):
        if chain[i][1] == 'R':
            link = hash_function(link + chain[i][0]).digest()
        elif chain[i][1] == 'L':
            link = hash_function(chain[i][0] + link).digest()
    if link == chain[-1][0]:
        return link
    else:
        raise AssertionError('The Merkle Chain is not valid')


def check_hex_chain(chain):
    """Verify a merkle chain, presented in hex form to see if the Merkle root can be reproduced.
    """
    return check_chain([(i[0].decode('hex'), i[1]) for i in chain]).encode('hex')


def join_chains(low, high):
    """Join two hierarchical merkle chains in the case where the root of a lower tree is an input
    to a higher level tree. The resulting chain should check out using the check functions.
    """
    return low[:-1] + high[1:]

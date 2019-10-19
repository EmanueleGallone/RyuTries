import itertools

STRIDE = 3


class MultibitNode(object):
    def __init__(self):
        self.children = {}

    def add(self, prefix, path):

        if path == "":
            return

        first = ""
        if len(path) > STRIDE:  # INCOMPLETE. TAKE A LOOK HERE
            first = path[:STRIDE]

        # first = path[:STRIDE]

        if path[STRIDE:] == "":  # if there is only 1 chunk

            if len(first) < STRIDE:
                self.children[first] = (prefix, None)
            else:
                for combination in GetCombinations(STRIDE - len(first)):
                    self.children[first + combination] = (prefix, None)

        else:  # there are more chunks
            if first not in self.children:
                self.children[first] = ("", MultibitNode())
            else:
                self.children[first] = (self.children[first][0], MultibitNode())

            self.children[first][1].add(prefix, path[STRIDE:])

    def lookup(self, address, backtrack=""):
        if len(address) < STRIDE:
            return backtrack

        first = address[:STRIDE]

        if len(address) < STRIDE or first not in self.children:
            return backtrack

        child = self.children[first]

        if len(address) == STRIDE or child[1] is None:
            return child[0]  # child.Item1 in C#

        else:
            if child[0] == "":
                return child[1].lookup(address[STRIDE:], backtrack)
            else:
                return child[1].lookup(address[STRIDE:], child[1])


def GetCombinations(length):
    # creating the combinations of the remaining bits
    char_set = [0, 1]
    return [''.join(map(str, i)) for i in itertools.product(char_set, repeat=length)]


if __name__ == "__main__":

    root = MultibitNode()

    # with open("db2.txt", 'r') as f:  # reading for creating
    #     my_list = [line.rstrip('\n') for line in f]
    #
    # for entry in my_list:
    #     addr, binary_address = entry.split(",")
    #     root.add(addr, binary_address)


    ip, bin_addr = "253.9.96.147\\11,11111101000".split(",")
    root.add(ip, bin_addr)

    print (root.lookup(bin_addr, '0'))


    with open("tosearch2.txt", 'r') as f:  # reading for lookups
        my_list = [line.rstrip('\n') for line in f]

    for entry in my_list:
        addr, binary_address = entry.split(",")
        print root.lookup(binary_address, "0")

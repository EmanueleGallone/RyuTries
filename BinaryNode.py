import timeit


class BinaryNode(object):
    def __init__(self, NextHop=""):
        self.NextHop = NextHop  # here we save the value of the leaf node
        self.Left = None  # 0's branch
        self.Right = None  # 1's branch

    def AddChild(self, prefix, path):
        if len(path) == 0:
            return

        if len(path) == 1:
            if path == "0":
                self.Left = BinaryNode(NextHop=prefix)
            else:
                self.Right = BinaryNode(NextHop=prefix)
        elif len(path) > 1:
            if path.startswith("0"):
                if self.Left is None:
                    self.Left = BinaryNode()

                self.Left.AddChild(prefix, path[1:])

            else:
                if self.Right is None:
                    self.Right = BinaryNode()

                self.Right.AddChild(prefix, path[1:])


    def Lookup(self, address, backtrack=""):
        if self.NextHop != "":
            backtrack = self.NextHop

        if address == "" or (self.Left is None and self.Right is None):
            return backtrack

        if address.startswith("0"):
            if self.Left is not None:
                return self.Left.Lookup(address[1:], backtrack)
            else:
                return backtrack
        else:
            if self.Right is not None:
                return self.Right.Lookup(address[1:], backtrack)
            else:
                return backtrack


def convert_in_bin(address):
    if address.find('\\') != -1:
        ip = address.split("\\")[0]
        mask = int(address.split("\\")[1])
        return ''.join([bin(int(x) + 256)[3:] for x in ip.split('.')])[:mask]
    else:
        return ''.join([bin(int(x) + 256)[3:] for x in address.split('.')])


def _is_binary(string):
    is_binary = True
    try:
        int(string, 2)
    except ValueError:
        is_binary = False
    return is_binary


# DEBUG
if __name__ == "__main__":

    root = BinaryNode("0")

    with open("db2.txt", 'r') as f:
        my_list = [line.rstrip('\n') for line in f]

    for address in my_list:
        addr = address.split(',')[0]
        binary_address = address.split(',')[1]
        ip = addr.split("\\")[0]
        mask = int(addr.split("\\")[1])
        addr = convert_in_bin(ip)[:mask]

        root.AddChild(ip, addr)

    with open('tosearch2.txt', 'r') as t:
        my_list = [line.rstrip('\n') for line in t]

    times = []
    for entry in my_list:
        addr = entry.split(",")[0]
        ip = addr.split("\\")[0]
        mask = int(addr.split("\\")[1])
        binary_address = convert_in_bin(ip)[:mask]

        start = timeit.default_timer()
        root.Lookup(binary_address)
        end = timeit.default_timer() - start
        times.append(end * 1000)

    print ("binary trie: " + str(sum(times)) + "ms")
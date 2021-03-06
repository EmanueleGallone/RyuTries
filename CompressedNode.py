import timeit

class CompressedNode(object):
    def __init__(self, NextHop="", Segment=""):
        self.NextHop = NextHop
        self.Left = None  # 0's branch
        self.Right = None  # 1's branch
        self.Segment = Segment
        self.Skip = len(Segment)

    def AddChild(self, prefix, path):
        if len(path) == 0:
            return

        if len(path) == 1:
            if path == "0":
                self.Left = CompressedNode(NextHop=prefix)
            else:
                self.Right = CompressedNode(NextHop=prefix)
        elif len(path) > 1:
            if path.startswith("0"):
                if self.Left is None:
                    self.Left = CompressedNode()

                self.Left.AddChild(prefix, path[1:])

            else:
                if self.Right is None:
                    self.Right = CompressedNode()

                self.Right.AddChild(prefix, path[1:])

    def Lookup(self, address, backtrack=""):
        # this lookup looks exactly the same as the one on BinaryNode with the only exception that we have
        # to take account of the skips
        if self.NextHop != "":
            backtrack = self.NextHop

        if address == "" or (self.Left is None and self.Right is None):
            return backtrack

        if address.startswith("0"):
            if self.Left is not None and (len(address) >= self.Left.Skip + 1) and (self.Left.Segment == "" or address.startswith("0" + self.Left.Segment)):
                return self.Left.Lookup(address[self.Left.Skip + 1:], backtrack)
            else:
                return backtrack
        else:
            if self.Right is not None and (len(address) >= self.Right.Skip + 1) and (self.Right.Segment == "" or address.startswith("1" + self.Right.Segment)):
                return self.Right.Lookup(address[self.Right.Skip + 1:], backtrack)
            else:
                return backtrack

    def LookupNonRecursive(self, address, rootPrefix="0"):
        backtrack = ""
        partialAddress = address
        node = self

        while node is not None:
            if node.NextHop != "":
                backtrack = node.NextHop

            if partialAddress == "" or (node.Left is None and node.Right is None):
                return backtrack

            if partialAddress.startswith("0"):
                if node.Left is not None and len(partialAddress) >= node.Left.Skip +1 and (node.Left.Segment == "" or partialAddress.startswith("0" + node.Left.Segment)):
                    partialAddress = partialAddress[node.Left.Skip+1:]
                    node = node.Left
                else:
                    return backtrack
            else:
                if node.Right is not None and len(partialAddress) >= node.Right.Skip + 1 and (node.Right.Segment == "" or partialAddress.startswith("0" + node.Right.Segment)):
                    partialAddress = partialAddress[node.Right.Skip+1:]
                    node = node.Right
                else:
                    return backtrack

        return backtrack

    def Compress(self, segment=""):

        # if I have no children, return myself
        if self.Right is None and self.Left is None:
            self.Segment = segment
            return self

        # If I have two children I cannot compress but I can call the compress method on my children
        if self.Right is not None and self.Left is not None:
            self.Right = self.Right.Compress("")
            self.Left = self.Left.Compress("")
            self.Segment = segment
            return self

        # SECTION: One Child only


        # If I am a prefix I stop compression and start compressing the child with empty segment
        if self.NextHop != "":
            self.Segment = segment

            if self.Left is not None:
                self.Left = self.Left.Compress("")
            elif self.Right is not None:
                self.Right = self.Right.Compress("")

            return self

        else:
            if self.Left is not None:
                return self.Left.Compress(segment + '0')
            else:
                return self.Right.Compress(segment + '1')


def convert_in_bin(address):
    # simple method to convert an IP address in its binary representation

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

def Create(default_value = '0'):
    _root = CompressedNode(default_value)

    with open("db.txt", 'r') as f:
        my_list = [line.rstrip('\n') for line in f]

    for address in my_list:
        addr, binary = address.split(',')
        ip, mask = addr.split("\\")

        _root.AddChild(ip, binary)

    _root.Compress()
    return _root


def __create_random_ip_list(list_length=10000, for_creating_tries=True):
    # creating set of ips for creating/searching tries.
    import random

    if for_creating_tries:
        with open('db.txt', 'w') as f:
            for i in range(1, list_length):
                ip = '{}.{}.{}.{}'.format(*__import__('random').sample(range(0, 255), 4))
                mask = str(random.choice([8, 12, 16, 24, 28]))
                f.write(ip + "\\" + mask + "," + convert_in_bin(ip)[:int(mask)] + "\n")
    else:  # else it means that it is for searching
        with open('to_search.txt', 'w') as f:
            for i in range(1, list_length):
                ip = '{}.{}.{}.{}'.format(*__import__('random').sample(range(0, 255), 4))
                mask = str(random.choice([8, 12, 16, 24, 28]))
                f.write(ip + "\\" + mask + "," + convert_in_bin(ip)[:mask] + "\n")


# DEBUG
if __name__ == "__main__":

    root = Create("0")

    with open('tosearch.txt', 'r') as t:
        my_list = [line.rstrip('\n') for line in t]


    times = []
    for entry in my_list:
        binary_address = entry.split(',')[1]

        start = timeit.default_timer()
        root.Lookup(binary_address)
        end = timeit.default_timer() - start
        times.append(end*1000)

    print("compressed trie: " + str(sum(times)) + "ms")

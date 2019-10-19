import itertools
import timeit

STRIDE = 3


class MultibitNode(object):
    def __init__(self):
        self.children = {}

    def AddChild(self, prefix, path):

        if path == "":
            return

        if len(path) < STRIDE:  # if the path is shorter than the stride

            # Expand the combinations and insert them all as children
            for combination in GetCombinations(STRIDE - len(path)):
                self.children[path + combination] = (prefix, None)

        elif len(path) == STRIDE: # If it's exactly as long as the stride
            
            # Set the corresponding dictionary entry
            self.children[path] = (prefix, None)

        else:  # if it's longer than the stride
            
            first = path[:STRIDE] # Take only the first STRIDE characters
            
            # If we don't have this value in the dictionary yet, make a new node with no prefix
            if first not in self.children:
                self.children[first] = ("", MultibitNode())
            # Otherwise keep the existing prefix and just create a child node
            else:
                self.children[first] = (self.children[first][0], MultibitNode())

            self.children[first][1].AddChild(prefix, path[STRIDE:])

    def Lookup(self, address, backtrack=""):
        if len(address) < STRIDE:
            return backtrack

        first = address[:STRIDE]

        # If the child does not exist, return last valid prefix
        if len(address) < STRIDE or first not in self.children:
            return backtrack

        child = self.children[first]

        # We're here when address is at least as long as the stride
        
        # If it's as long as the stride, or there is no pointer to another multibit node
        if len(address) == STRIDE or child[1] is None:
            return child[0]

        else:
            if child[0] == "":
                return child[1].Lookup(address[STRIDE:], backtrack)
            else:
                return child[1].Lookup(address[STRIDE:], child[0])


def GetCombinations(length):
    # creating the combinations of the remaining bits
    char_set = [0, 1]
    return [''.join(map(str, i)) for i in itertools.product(char_set, repeat=length)]

def Create():
    _root = MultibitNode()
    with open("db.txt", 'r') as f:  # reading for creating
        my_list = [line.rstrip('\n') for line in f]

    for entry in my_list:
        addr, binary_address = entry.split(",")
        _root.AddChild(addr, binary_address)

    return _root


if __name__ == "__main__":

    root = Create()

    # Qui stiamo cercando 000. Se non lo trova usiamo il backtrack Default
    # print (root.lookup("000", 'Default'))
    
    # Qui stiamo cercando 010. Se non lo trova usiamo il backtrack Default altrimenti printa l'ip per intero
    # print (root.lookup("010", "Default"))
    
    # L'indirizzo che usavi tu aveva una mask non multipla di 3 quindi fa casino quando va a cercarlo, ricordi? Quindi fa sempre backtrack sul Default!


    with open("tosearch.txt", 'r') as f:  # reading for lookups
       my_list = [line.rstrip('\n') for line in f]

    times = []
    for entry in my_list:  # lookup timing
       addr, binary_address = entry.split(",")

       start = timeit.default_timer()  # starting timing
       root.Lookup(binary_address, "0")
       end = timeit.default_timer() - start

       times.append(end*1000)

    print ("MultibitTrie: " + str(sum(times)) + "ms")

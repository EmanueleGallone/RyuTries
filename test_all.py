import BinaryNode
import CompressedNode
import MultibitNode
import timeit

binary_root = BinaryNode.Create('0')
compressed_root = CompressedNode.Create("0")
multibit_root = MultibitNode.Create()

# starting performing lookups
with open('tosearch.txt', 'r') as t:
    my_list = [line.rstrip('\n') for line in t]

times = []
for entry in my_list:
    binary_address = entry.split(',')[1]

    start = timeit.default_timer()
    binary_root.Lookup(binary_address)
    end = timeit.default_timer() - start
    times.append(end * 1000)

print("binary_trie (avg per lookup): " + str(sum(times)/len(times)) + "ms")
print("binary_trie (sum of all times): " + str(sum(times)) + "ms")

times = []
for entry in my_list:
    binary_address = entry.split(',')[1]

    start = timeit.default_timer()
    compressed_root.Lookup(binary_address)
    end = timeit.default_timer() - start
    times.append(end * 1000)

print("compressed trie (avg per lookup): " + str(sum(times)/len(times)) + "ms")
print("compressed trie (sum of all times): " + str(sum(times)) + "ms")

times = []
for entry in my_list:
    binary_address = entry.split(',')[1]

    start = timeit.default_timer()
    multibit_root.Lookup(binary_address, "0")
    end = timeit.default_timer() - start
    times.append(end * 1000)

print("multibit trie (avg per lookup): " + str(sum(times)/len(times)) + "ms")
print("multibit trie (sum of all times): " + str(sum(times)) + "ms")

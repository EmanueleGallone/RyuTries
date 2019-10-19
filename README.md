### Tries data structures made for IP lookups in Ryu Framework

### OLD

## Getting started
### Binary Trie

#### Usage:
```
import BinaryTrie
```

use custom prefix table (only dictionary should be used):
- NB: the custom table must have the binary representation of a prefix ip address
```
custom_table = {"1100001":"192.168.0.1", "110000": "192.168.0.10"}
BinaryTrie.TABLE = custom_table
```

create the Binary Trie:
```
trie = BinaryTrie.TrieNode('', 'Default_Value')
trie = BinaryTrie.create()
```

find longest prefix match:
```
BinaryTrie.find_longest_prefix(trie, '001')
```
#

### Multibit Trie
#### Usage:
```
import MultibitTrie
```
You can change the TABLE dictionary using custom prefixes:
```
custom_table = {"P1":"", "P2":"001, "P3":"010"}
MultibitTrie.TABLE = custom_table
```
NB: make sure you have a prefix as default, in my case "P1".
the default value can be overridden when creating the trie (see section 'Create the Trie' below)

You can also change the Stride of the Trie:
```
MultibitTrie.STRIDE = 2
```

Create the Trie:(the '*' is the default value that is returned in case no other prefix is found)
```
root = MultibitTrie.TrieNode('*')
MultibitTrie.initialize(root)
```

find longest prefix match:
```
MultibitTrie.longest_prefix(root, '001')
```
will return:
```
('001','P2')
```
#

### Compressed Trie
Notes: 
- this trie returns 0 when a prefix is not found
- use 'find_longest_prefix' method to find a prefix. It returns a node object
- if you need the value of the prefix just use trie.find_longest_prefix(trie).label
#### Usage:
```
import CompressedTrie
```
change the TABLE for constructing the trie, using custom prefixes:
```
custom_table = {"1100001"}
CompressedTrie.TABLE = custom_table
```

Create the Trie:
```
root = CompressedTrie.create()
```

Find the longest prefix:
```
prefix_node = CompressedTrie.find_longest_prefix(root, '192.168.0.1')
```

the attribute 'label' is used to show the prefix name:
```
print(prefix_node.label) -> P1
```


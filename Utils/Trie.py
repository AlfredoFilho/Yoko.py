'''
Implementation from: https://github.com/Novandev/

Read more:

https://medium.com/@donovan.adams/you-trie-d-it-an-introduction-to-tries-and-its-applications-in-python-97802e8fc12e
https://github.com/Novandev/CS-2.1-Advanced-Trees-and-Sorting-Algorithms/blob/master/autocommplete/trie.py
'''

class CharNode(object):
    """This class keeps track of if a node is at the end of the tree of possible combinations"""

    def __init__(self):
        self.end = False
        self.children = {}

    def all_words_from_current_node(self, prefix):

        if self.end:
            yield prefix

        for letter, childNodes in self.children.items():
            yield from childNodes.all_words_from_current_node(prefix + letter)


class Trie:

    def __init__(self):
        self.root = CharNode()

    def add(self, word):

        curr = self.root
        for ch in word:
            node = curr.children.get(ch)
            if not node:
                node = CharNode()
                curr.children[ch] = node
            curr = node
        curr.end = True

    def search(self, search_word):

        if len(self.root.children) == {}:
            raise ValueError(
                "The dictionary is empty, please add words via the add method")
        curr = self.root
        for letter in search_word:
            node = curr.children.get(letter)
            if not node:
                return False
            curr = node
        return curr.end
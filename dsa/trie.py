class TrieNode:

    def __init__(self):
        self.charToNode = {} # key: char, val: node
        self.endOfWord = False

    def insert(self, word):
        node = self
        for ch in word:
            if ch not in node.charToNode:
                node.charToNode[ch] = TrieNode()
            node = node.charToNode[ch]
        node.endOfWord = True
    
    """
    Search for exact word
    """
    def search(self, word):
        node = self
        for ch in word:
            if ch not in node.charToNode:
                return False
            node = node.charToNode[node]
        return node.endOfWord

    def startsWith(self, prefix):
        node = self
        for ch in prefix:
            if ch not in node.charToNode:
                return False
            node = node.charToNode[node]
        return True
        
    
INITIAL_CAPACITY = 50

class Node:
    def __init__(self, key, val, next=None):
        self.key = key
        self.val = val
        self.next = next


class HashTable:
    def __init__(self):
        self.capacity = INITIAL_CAPACITY
        self.size = 0
        self.buckets = [None] * self.capacity

    """
    Hash Function: Add (index + length of key) ** (curr char code)
    Perform modulo to keep hashsum in range
    """
    def hash(self, key):
        hash_sum = 0
        for idx, char in enumerate(key):
            hash_sum += (idx + len(key)) ** ord(char)
        return hash_sum % self.capacity

    def insert(self, key, val):
        
        self.size += 1

        idx = self.hash(key)

        node = self.buckets[idx]

        # Check for the state of the bucket 
        if not node:
            # Initialise new node
            self.buckets[idx] = Node(key, val)
            return
        # Collision happen -> Insert to the end of LL
        else:
            curr = self.buckets[idx]
            # Iterate until the tail of the LL
            while curr.next:
                curr = curr.next
            # Add new node to key, val
            curr.next = Node(key, val)
            
    def find(self, key):

        idx = self.hash(key)

        node = self.buckets[idx]
        # Iterate through LL to check if the target val has been reached
        curr = node
        while curr:
            if curr.key == key:
                return curr.val
            curr = curr.next
        return None
    
    def delete(self, key):
        idx = self.hash(key)

        node = self.buckets[idx]

        if not node:
            return None

        if node.key == key:
            self.buckets[idx] = node.next
            self.size -= 1
            return

        # Iterate through LL to delete key
        prev, curr = None, node

        while curr:
            if curr.key == key:
                self.size -= 1
                prev.next = curr.next
                return
            prev = curr
            curr = curr.next
        
        return None

hash_table = HashTable()
hash_table.insert("test", 3)
hash_table.insert("meme", 500)
hash_table.delete("test")
print(hash_table.find("test"))
print(hash_table.find("meme"))
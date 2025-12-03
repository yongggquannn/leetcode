class ListNode:
    def __init__(self, val=0, next=None):    
        self.val = val
        self.next = next

# Deletion method

def delete_node(head, target):
    # Base case: Check if head of LL is the target
    if head.val == target:
        return head.next
    
    # Iterate through each node in LL to find the target
    prev, curr = None, head

    while curr:
        if curr.val == target:
            prev.next = curr.next
            break
        prev = curr
        curr = curr.next
    
    return head

# Traversing LL (E.g. To find length of LL)

def find_length(head):
    res = 0
    curr = head
    while curr:
        res += 1
        curr = curr.next
    return res


"""
1 -> 2 -> 3 -> 4

1 -> 3 -> 4

Delete Node 2:
prev: 1 
curr: 2

Length of LL:
res : 4
curr: None
"""